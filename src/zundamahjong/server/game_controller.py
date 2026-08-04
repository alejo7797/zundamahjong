from random import sample
from threading import Lock
from time import sleep
from typing import final

from pydantic import BaseModel

from ..mahjong.action import Action
from ..mahjong.game import Game
from ..mahjong.game_options import GameOptions
from ..mahjong.info import AllGameInfo, HistoryItem
from ..types.player import BotPlayer, Player
from .sio import sio


class AllInfo(BaseModel):
    """
    Represents all the info a player should have, including avatars of players.
    """

    all_game_info: AllGameInfo
    history_updates: list[HistoryItem]
    players: list[Player]


@final
class GameController:
    """
    Controls a game of mahjong and handles sending game information to players.

    :param players: A list of the players who will play the game.
    :param options: The game options to use for the game.
    """

    def __init__(self, players: list[Player], options: GameOptions) -> None:
        self._players = sample(players, len(players))
        self._game = Game(options=options)
        self._lock = Lock()
        with self._lock:
            self._emit_info_all_inner(self._game.round.history)
        self.perform_bot_actions()

    @property
    def game(self) -> Game:
        """The underlying :py:class:`Game` object."""
        return self._game

    def emit_info(self, player: Player) -> None:
        """
        Send game info to one of the players playing the game.

        :param player: The player to send info to.
        """
        with self._lock:
            index = self._get_player_index(player)
            sio.emit("info", self._info(index, []).model_dump(), to=player.id)

    def submit_action(
        self, player: Player, action: Action, history_index: int, is_user: bool = True
    ) -> list[tuple[int, Action]] | None:
        """
        Submit a player's action to the game.

        :param player: The player submitting the action.
        :param action_data: The :py:class:`Action` the player is submitting.
        :param history_index: The moment within the game when they are submitting
                            the action, measured in terms of number of actions
                            in the game's history.
        """
        with self._lock:
            player_index = self._get_player_index(player)
            history_updates = self._game.submit_action(
                player_index, action, history_index
            )
            if history_updates is not None and len(history_updates) > 0:
                self._emit_info_all_inner(history_updates)
        if is_user:
            self.perform_bot_actions()
        return history_updates

    def start_next_round(self, player: Player) -> None:
        """
        Start the next round of the game.

        :param player: The player starting the next round.
                       This will raise an exception if this is not one
                       of the players in the game.
        """
        with self._lock:
            self._get_player_index(player)
            if not self._game.can_start_next_round:
                raise Exception("Cannot start next round!")
            self._game.start_next_round()
            self._emit_info_all_inner(self._game.round.history)
        self.perform_bot_actions()

    def perform_bot_actions(self) -> None:
        """
        Perform actions for bot players until the game state no longer advances.
        """
        player_index = 0
        # repeatedly perform bot actions,
        # in order of players
        while player_index < len(self._players):
            player = self._players[player_index]
            is_bot = isinstance(player, BotPlayer)
            if not is_bot:
                player_index += 1
                continue

            # make sure to only lock when getting info
            # in order to avoid deadlocks
            with self._lock:
                info = self._game.info(player_index)

            history_index = len(info.round_info.history)
            action_selected = info.player_info.action_selected
            if action_selected:
                player_index += 1
                continue

            if len(info.player_info.actions) == 0:
                # no possible actions (this implies the round has ended)
                player_index += 1
                continue

            # stupid bot, always performs first possible action
            if len(info.player_info.actions) > 1:
                sleep(0.5)
            action = info.player_info.actions[0]

            history_updates = self.submit_action(
                player, action, history_index, is_user=False
            )
            if history_updates is None:
                # submit_action failed, restart loop
                player_index = 0
                continue
            if len(history_updates) > 0:
                # submit_action changed the game state, restart loop
                player_index = 0
            else:
                # submit_action did not change the game state
                player_index += 1

    def _get_player_index(self, player: Player) -> int:
        try:
            return self._players.index(player)
        except ValueError:
            raise Exception(f"Player {player.id} not found in this game!")

    def _info(self, index: int, history_updates: list[tuple[int, Action]]) -> AllInfo:
        return AllInfo(
            all_game_info=self._game.info(index),
            players=self._players,
            history_updates=[
                HistoryItem(player_index=history_item[0], action=history_item[1])
                for history_item in history_updates
            ],
        )

    def _emit_info_all_inner(self, history_updates: list[tuple[int, Action]]) -> None:
        for index, player in enumerate(self._players):
            sio.emit(
                "info", self._info(index, history_updates).model_dump(), to=player.id
            )
