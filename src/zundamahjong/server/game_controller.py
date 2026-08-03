from random import sample
from threading import Lock
from typing import final

from pydantic import BaseModel

from ..mahjong.action import Action
from ..mahjong.game import Game
from ..mahjong.game_options import GameOptions
from ..mahjong.info import AllGameInfo, HistoryItem
from ..types.player import Player
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

    def submit_action(self, player: Player, action: Action, history_index: int) -> None:
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
