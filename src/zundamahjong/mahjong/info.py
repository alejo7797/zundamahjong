from collections.abc import Sequence

from pydantic import BaseModel

from .action import Action
from .call import Call
from .discard_pool import Discard
from .round import RoundStatus
from .scoring import Scoring
from .tile import TileId
from .win import Win


class GameInfo(BaseModel):
    """
    Represents the information about a game of mahjong that is retained
    across rounds.
    """

    wind_round: int
    sub_round: int
    draw_count: int
    player_scores: tuple[float, ...]


class HistoryItem(BaseModel):
    """
    Represents an action taken and the player who performed it in a round of Mahjong.
    """

    player_index: int
    action: Action


class RoundInfo(BaseModel):
    """
    Represents the public information at a given moment in a round of mahjong.
    """

    tiles_left: int
    current_player: int
    status: RoundStatus
    discards: list[Discard]
    history: list[HistoryItem]
    hand_counts: list[int]
    riichi_discard_indexes: list[int | None]
    calls: list[Sequence[Call]]
    flowers: list[Sequence[TileId]]
    dora: list[TileId]


class PlayerInfo(BaseModel):
    """
    Represents the information specific to a player during a round of mahjong.
    """

    hand: list[TileId]
    actions: list[Action]
    action_selected: bool
    is_furiten: bool


class AllGameInfo(BaseModel):
    """
    Represents all the game-related info a player should have at a given moment
    in a round of mahjong.
    """

    player_count: int
    player_index: int
    is_game_end: bool
    game_info: GameInfo
    round_info: RoundInfo
    player_info: PlayerInfo
    win_info: Win | None
    scoring_info: Scoring | None
