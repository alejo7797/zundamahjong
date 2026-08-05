from collections.abc import Sequence

from .action import Action, ActionType
from .call import get_call_tiles
from .info import AllGameInfo
from .shanten import calculate_shanten
from .tile import TileId, TileValue, all_tiles, get_tile_value, tile_id_is_flower


def calculate_bot_action(info: AllGameInfo) -> Action:
    """
    Given info on the bot's view of the game state,
    returns the action the bot chooses.

    :param info: An object with the info of the game state from the bot's point of view.
    """

    if len(info.player_info.actions) == 1:
        return info.player_info.actions[0]

    action_scores = {action: 0 for action in info.player_info.actions}

    # prioritise winning and flowers
    for action in action_scores:
        if (
            action.action_type == ActionType.RON
            or action.action_type == ActionType.TSUMO
            or action.action_type == ActionType.FLOWER
        ):
            action_scores[action] += 100000

    # add shanten scores
    if all(not tile_id_is_flower(tile) for tile in info.player_info.hand):
        freqs = unseen_frequencies(info)
        for action in action_scores:
            action_scores[action] += get_action_shanten_score(action, info, freqs)

    best_action, _ = max(action_scores.items(), key=lambda a: a[1])
    return best_action


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


def get_action_shanten_score(
    action: Action, info: AllGameInfo, freqs: dict[TileValue, int]
) -> int:
    if (
        action.action_type == ActionType.DISCARD
        or action.action_type == ActionType.RIICHI
        or action.action_type == ActionType.ADD_KAN
    ):
        return remove_tile_get_shanten_score(
            action.tile,
            info.player_info.hand,
            info,
            freqs,
        )
    if action.action_type == ActionType.CLOSED_KAN:
        new_hand = [t for t in info.player_info.hand if t not in action.tiles]
        return get_shanten_score(new_hand, info, freqs)
    if action.action_type == ActionType.PASS or action.action_type == ActionType.DRAW:
        return get_shanten_score(info.player_info.hand, info, freqs)
    if action.action_type == ActionType.CHII or action.action_type == ActionType.PON:
        new_hand = [t for t in info.player_info.hand if t not in action.other_tiles]
        return get_best_shanten_score(new_hand, info, freqs)
    if action.action_type == ActionType.OPEN_KAN:
        new_hand = [t for t in info.player_info.hand if t not in action.other_tiles]
        return get_shanten_score(new_hand, info, freqs)

    return 0


def get_shanten_score(
    hand: Sequence[TileId], info: AllGameInfo, freqs: dict[TileValue, int]
) -> int:
    (shanten, useful_tiles) = calculate_shanten(
        [get_tile_value(tile) for tile in hand], is_3player=(info.player_count == 3)
    )
    useful_tiles_count = sum(freqs[tile_value] for tile_value in useful_tiles)
    return -100 * shanten + useful_tiles_count


def remove_tile_get_shanten_score(
    tile: TileId, hand: Sequence[TileId], info: AllGameInfo, freqs: dict[TileValue, int]
) -> int:
    new_hand = [t for t in hand if t != tile]
    return get_shanten_score(new_hand, info, freqs)


def get_best_shanten_score(
    hand: Sequence[TileId], info: AllGameInfo, freqs: dict[TileValue, int]
) -> int:
    return max(remove_tile_get_shanten_score(tile, hand, info, freqs) for tile in hand)
