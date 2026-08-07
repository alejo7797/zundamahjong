from .pattern_calculator import PatternCalculator, register_pattern


@register_pattern(
    "BLESSING_OF_HEAVEN",
    display_name="Blessing of Heaven",
    yaku=20,
)
def blessing_of_heaven(self: PatternCalculator) -> int:
    "Win on the dealer's first draw."
    return int(self.win.is_tenhou)


@register_pattern(
    "BLESSING_OF_EARTH",
    display_name="Blessing of Earth",
    yaku=19,
)
def blessing_of_earth(self: PatternCalculator) -> int:
    "Win on a nondealer's first draw."
    return int(self.win.is_chiihou)


@register_pattern(
    "RIICHI",
    display_name="Riichi",
    yaku=1,
)
def riichi(self: PatternCalculator) -> int:
    "Win after calling riichi."
    return int(self.win.is_riichi and not self.win.is_double_riichi)


@register_pattern(
    "DOUBLE_RIICHI",
    display_name="Double Riichi",
    yaku=2,
)
def double_riichi(self: PatternCalculator) -> int:
    "Win after calling riichi on the first turn."
    return int(self.win.is_double_riichi)


@register_pattern(
    "IPPATSU",
    display_name="Ippatsu",
    yaku=1,
)
def ippatsu(self: PatternCalculator) -> int:
    "Win immediately after calling riichi."
    return int(self.win.is_ippatsu)


@register_pattern(
    "ROBBING_A_KAN",
    display_name="Robbing a Kan",
    yaku=1,
)
def robbing_a_kan(self: PatternCalculator) -> int:
    "Win by stealing from another player's kan."
    return int(self.win.is_chankan)


@register_pattern(
    "UNDER_THE_SEA",
    display_name="Under the Sea",
    yaku=1,
)
def under_the_sea(self: PatternCalculator) -> int:
    "Win on the last draw."
    return int(self.win.is_haitei)


@register_pattern(
    "UNDER_THE_RIVER",
    display_name="Under the River",
    yaku=1,
)
def under_the_river(self: PatternCalculator) -> int:
    "Win on the last discard."
    return int(self.win.is_houtei)


@register_pattern(
    "AFTER_A_FLOWER",
    display_name="After a Flower",
    yaku=1,
)
def after_a_flower(self: PatternCalculator) -> int:
    "Win on a tile drawn after replacing a flower."
    return self.win.after_flower_count


@register_pattern(
    "AFTER_A_KAN",
    display_name="After a Kan",
    yaku=2,
)
def after_a_kan(self: PatternCalculator) -> int:
    "Win on a tile drawn after calling a kan."
    return self.win.after_kan_count


@register_pattern(
    "DRAW",
    display_name="Draw",
    yaku=1,
)
def draw(self: PatternCalculator) -> int:
    "Win after a draw in the previous round."
    return self.win.draw_count
