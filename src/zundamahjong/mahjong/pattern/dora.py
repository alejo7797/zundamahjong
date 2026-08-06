from ..tile import TileId, TileValue, get_tile_value
from .pattern_calculator import PatternCalculator, register_pattern


def get_dora_value(tile: TileId, is_3player: bool) -> TileValue:
    value = get_tile_value(tile)
    if is_3player and value == 1:
        return 9
    if value < 30:
        if value % 10 == 9:
            return value - 8
        else:
            return value + 1
    elif value == 37:
        return 35
    else:
        if (value % 10) % 4 == 0:
            return value - 3
        else:
            return value + 1


@register_pattern(
    "DORA",
    display_name="Dora",
    han=1,
    fu=0,
)
def dora(self: PatternCalculator) -> int:
    """
    The number of (non-ura) dora tiles.
    """
    return sum(
        sum(
            1
            for tile in self.hand_tiles
            if get_tile_value(tile)
            == get_dora_value(dora_tile, self.win.player_count == 3)
        )
        for dora_tile in self.win.dora
    )
