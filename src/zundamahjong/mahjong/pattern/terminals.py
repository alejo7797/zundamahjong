from ..tile import is_number, terminals
from .pattern_calculator import PatternCalculator, register_pattern
from .wait_pattern import WaitPattern


@register_pattern(
    "ALL_SIMPLES",
    display_name="All Simples",
    yaku=1,
)
def all_simples(self: PatternCalculator) -> int:
    """
    The hand does not use any terminal or honour tiles.
    """
    return int(
        all((is_number(tile) and 2 <= tile % 10 <= 8) for tile in self.hand_tiles)
    )


@register_pattern(
    "HALF_OUTSIDE_HAND",
    display_name="Half Outside Hand",
    yaku=2,
)
def half_outside_hand(self: PatternCalculator) -> int:
    """
    Every meld and pair uses a terminal or honour tile, and both
    terminals and honours are used.
    """
    return int(self.call_outsidenesses == {1, 2})


@register_pattern(
    "FULLY_OUTSIDE_HAND",
    display_name="Fully Outside Hand",
    yaku=4,
)
def fully_outside_hand(self: PatternCalculator) -> int:
    """
    Every meld and pair uses a terminal tile.
    """
    return int(self.call_outsidenesses == {2})


@register_pattern(
    "ALL_TERMINALS_AND_HONOURS",
    display_name="All Terminals and Honours",
    yaku=3,
)
def all_terminals_and_honours(self: PatternCalculator) -> int:
    """
    Every tile is a terminal or honour tile, and both terminals and honours
    are used.
    """
    return int(
        len(self.chii_start_tiles) == 0
        and half_outside_hand(self)
        and not (thirteen_orphans(self) or thirteen_orphans_13_sided_wait(self))
    )


@register_pattern(
    "ALL_TERMINALS",
    display_name="All Terminals",
    yaku=13,
)
def all_terminals(self: PatternCalculator) -> int:
    """
    Every tile is a terminal tile.
    """
    return int(all(tile in terminals for tile in self.hand_tiles))


@register_pattern(
    "THIRTEEN_ORPHANS",
    display_name="Thirteen Orphans",
    yaku=13,
)
def thirteen_orphans(self: PatternCalculator) -> int:
    """
    The hand consists of every terminal and honour tile, plus one extra
    terminal or honour tile, and the winning tile is not the extra tile
    (this is a special hand structure).
    """
    return int(self.wait_pattern == WaitPattern.KOKUSHI)


@register_pattern(
    "THIRTEEN_ORPHANS_13_SIDED_WAIT",
    display_name="Thirteen Orphans 13-sided Wait",
    yaku=13,
)
def thirteen_orphans_13_sided_wait(self: PatternCalculator) -> int:
    """
    The hand consists of every terminal and honour tile, plus one extra
    terminal or honour tile, and the winning tile is the extra tile
    (this is a special hand structure).
    """
    return int(self.wait_pattern == WaitPattern.KOKUSHI_13)
