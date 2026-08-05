from time import sleep

from .action import Action
from .call import get_call_tiles
from .info import AllGameInfo, RoundInfo
from .tile import TileValue, all_tiles, get_tile_value


def calculate_bot_action(info: AllGameInfo) -> Action:
    """
    Given info on the bot's view of the game state,
    returns the action the bot chooses.

    :param info: An object with the info of the game state from the bot's point of view.
    """

    if len(info.player_info.actions) == 1:
        return info.player_info.actions[0]

    sleep(0.5)
    return info.player_info.actions[0]


def unseen_frequencies(info: AllGameInfo) -> dict[TileValue, int]:
    freqs = {tile_value: 4 for tile_value in all_tiles}

    for tile in info.player_info.hand:
        freqs[get_tile_value(tile)] -= 1
    for player_calls in info.round_info.calls:
        for call in player_calls:
            for tile in get_call_tiles(call):
                freqs[get_tile_value(tile)] -= 1
    for discard in info.round_info.discards:
        if (
            not discard.is_called
            and not discard.is_added_kan
            and not discard.is_closed_kan
        ):
            freqs[get_tile_value(discard.tile)] -= 1

    return freqs
