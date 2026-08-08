import unittest

from tests.decks import (
    test_deck1,
    test_deck2,
    test_deck3,
    test_deck4,
    test_deck5,
    test_deck_haitei,
    test_deck_kan_tenhou,
    test_deck_rinshan1,
    test_deck_rinshan2,
)
from zundamahjong.mahjong.action import (
    Action,
    ActionType,
    AddKanAction,
    ClosedKanAction,
    HandTileAction,
    OpenCallAction,
    OpenKanAction,
    SimpleAction,
)
from zundamahjong.mahjong.call import (
    AddKanCall,
    CallType,
    ClosedKanCall,
    OpenCall,
    OpenKanCall,
)
from zundamahjong.mahjong.game_options import GameOptions
from zundamahjong.mahjong.round import Round, RoundStatus


class RoundTest(unittest.TestCase):
    def test_start(self) -> None:
        round = Round(tiles=test_deck1)
        assert round.current_player == 0
        assert round.status == RoundStatus.PLAY
        assert round.discard_tiles == []
        assert round.history == [
            (0, SimpleAction(action_type=ActionType.CONTINUE)),
            (1, SimpleAction(action_type=ActionType.CONTINUE)),
            (2, SimpleAction(action_type=ActionType.CONTINUE)),
            (3, SimpleAction(action_type=ActionType.CONTINUE)),
            (0, SimpleAction(action_type=ActionType.CONTINUE)),
        ]

    def test_fixed_deck_start_hands(self) -> None:
        round = Round(tiles=test_deck1)
        assert round.get_hand(0) == [
            10,
            12,
            20,
            30,
            40,
            50,
            60,
            70,
            80,
            90,
            170,
            210,
            211,
            212,
        ]
        assert round.get_hand(1) == [
            11,
            21,
            31,
            41,
            51,
            61,
            71,
            81,
            91,
            92,
            93,
            171,
            213,
        ]
        assert round.get_hand(2) == [
            110,
            111,
            112,
            113,
            130,
            131,
            132,
            133,
            150,
            151,
            152,
            153,
            172,
        ]
        assert round.get_hand(3) == [
            120,
            121,
            122,
            123,
            140,
            141,
            142,
            143,
            160,
            161,
            162,
            163,
            173,
        ]

    def test_sub_round_start_hands(self) -> None:
        round = Round(tiles=test_deck1, sub_round=1)
        assert round.get_hand(1) == [
            10,
            12,
            20,
            30,
            40,
            50,
            60,
            70,
            80,
            90,
            170,
            210,
            211,
            212,
        ]
        assert round.get_hand(2) == [
            11,
            21,
            31,
            41,
            51,
            61,
            71,
            81,
            91,
            92,
            93,
            171,
            213,
        ]
        assert round.get_hand(3) == [
            110,
            111,
            112,
            113,
            130,
            131,
            132,
            133,
            150,
            151,
            152,
            153,
            172,
        ]
        assert round.get_hand(0) == [
            120,
            121,
            122,
            123,
            140,
            141,
            142,
            143,
            160,
            161,
            162,
            163,
            173,
        ]

    def test_discard_pool(self) -> None:
        round = Round(tiles=test_deck1)
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=170))
        assert round.discard_tiles == [170]

    def test_discard_hand(self) -> None:
        round = Round(tiles=test_deck1)
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=170))
        assert round.get_hand(0) == [
            10,
            12,
            20,
            30,
            40,
            50,
            60,
            70,
            80,
            90,
            210,
            211,
            212,
        ]

    def test_draw(self) -> None:
        round = Round(tiles=test_deck1)
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=170))
        round.do_action(1, SimpleAction(action_type=ActionType.DRAW))
        assert round.get_hand(1) == [
            11,
            21,
            31,
            41,
            51,
            61,
            71,
            81,
            91,
            92,
            93,
            171,
            213,
            13,
        ]

    def test_chi_a(self) -> None:
        round = Round(tiles=test_deck1)
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=50))
        round.do_action(
            1,
            OpenCallAction(action_type=ActionType.CHII, other_tiles=(61, 71)),
        )
        assert round.get_hand(1) == [11, 21, 31, 41, 51, 81, 91, 92, 93, 171, 213]
        assert round.get_calls(1) == [
            OpenCall(
                call_type=CallType.CHI,
                called_player_index=0,
                called_tile=50,
                other_tiles=(61, 71),
            )
        ]
        round.do_action(1, HandTileAction(action_type=ActionType.DISCARD, tile=21))
        assert round.discard_tiles == [21]

    def test_chi_b(self) -> None:
        round = Round(tiles=test_deck1)
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=50))
        round.do_action(
            1, OpenCallAction(action_type=ActionType.CHII, other_tiles=(41, 61))
        )
        assert round.get_hand(1) == [11, 21, 31, 51, 71, 81, 91, 92, 93, 171, 213]
        assert round.get_calls(1) == [
            OpenCall(
                call_type=CallType.CHI,
                called_player_index=0,
                called_tile=50,
                other_tiles=(41, 61),
            )
        ]
        round.do_action(1, HandTileAction(action_type=ActionType.DISCARD, tile=21))
        assert round.discard_tiles == [21]

    def test_chi_c(self) -> None:
        round = Round(tiles=test_deck1)
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=50))
        round.do_action(
            1, OpenCallAction(action_type=ActionType.CHII, other_tiles=(31, 41))
        )
        assert round.get_hand(1) == [11, 21, 51, 61, 71, 81, 91, 92, 93, 171, 213]
        assert round.get_calls(1) == [
            OpenCall(
                call_type=CallType.CHI,
                called_player_index=0,
                called_tile=50,
                other_tiles=(31, 41),
            )
        ]
        round.do_action(1, HandTileAction(action_type=ActionType.DISCARD, tile=21))
        assert round.discard_tiles == [21]

    def test_pon(self) -> None:
        round = Round(tiles=test_deck1)
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=90))
        round.do_action(
            1, OpenCallAction(action_type=ActionType.PON, other_tiles=(91, 92))
        )
        assert round.get_hand(1) == [11, 21, 31, 41, 51, 61, 71, 81, 93, 171, 213]
        assert round.get_calls(1) == [
            OpenCall(
                call_type=CallType.PON,
                called_player_index=0,
                called_tile=90,
                other_tiles=(91, 92),
            )
        ]
        round.do_action(1, HandTileAction(action_type=ActionType.DISCARD, tile=21))
        assert round.discard_tiles == [21]

    def test_pon_change_turn(self) -> None:
        round = Round(tiles=test_deck1)
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=10))
        round.do_action(1, SimpleAction(action_type=ActionType.DRAW))
        round.do_action(1, HandTileAction(action_type=ActionType.DISCARD, tile=213))
        round.do_action(
            0, OpenCallAction(action_type=ActionType.PON, other_tiles=(210, 211))
        )
        assert round.get_hand(0) == [12, 20, 30, 40, 50, 60, 70, 80, 90, 170, 212]
        assert round.get_calls(0) == [
            OpenCall(
                call_type=CallType.PON,
                called_player_index=1,
                called_tile=213,
                other_tiles=(210, 211),
            )
        ]
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=20))
        assert round.discard_tiles == [10, 20]

    def test_open_kan(self) -> None:
        round = Round(tiles=test_deck1)
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=90))
        round.do_action(1, OpenKanAction(other_tiles=(91, 92, 93)))
        assert round.get_hand(1) == [11, 21, 31, 41, 51, 61, 71, 81, 171, 213, 83]
        assert round.get_calls(1) == [
            OpenKanCall(called_player_index=0, called_tile=90, other_tiles=(91, 92, 93))
        ]
        round.do_action(1, HandTileAction(action_type=ActionType.DISCARD, tile=21))
        assert round.discard_tiles == [21]

    def test_open_kan_change_turn(self) -> None:
        round = Round(tiles=test_deck1)
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=10))
        round.do_action(1, SimpleAction(action_type=ActionType.DRAW))
        round.do_action(1, HandTileAction(action_type=ActionType.DISCARD, tile=213))
        round.do_action(0, OpenKanAction(other_tiles=(210, 211, 212)))
        assert round.get_hand(0) == [12, 20, 30, 40, 50, 60, 70, 80, 90, 170, 83]
        assert round.get_calls(0) == [
            OpenKanCall(
                called_player_index=1, called_tile=213, other_tiles=(210, 211, 212)
            )
        ]
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=20))
        assert round.discard_tiles == [10, 20]

    def test_add_kan(self) -> None:
        round = Round(tiles=test_deck1)
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=90))
        round.do_action(
            1, OpenCallAction(action_type=ActionType.PON, other_tiles=(91, 92))
        )
        round.do_action(1, HandTileAction(action_type=ActionType.DISCARD, tile=213))
        round.do_action(
            0, OpenCallAction(action_type=ActionType.PON, other_tiles=(210, 211))
        )
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=10))
        round.do_action(1, SimpleAction(action_type=ActionType.DRAW))
        round.do_action(
            1,
            AddKanAction(
                tile=93,
                pon_call=OpenCall(
                    call_type=CallType.PON,
                    called_player_index=0,
                    called_tile=90,
                    other_tiles=(91, 92),
                ),
            ),
        )
        assert round.get_hand(1) == [11, 13, 21, 31, 41, 51, 61, 71, 81, 171, 83]
        assert round.get_calls(1) == [
            AddKanCall(
                called_player_index=0,
                called_tile=90,
                added_tile=93,
                other_tiles=(91, 92),
            )
        ]
        round.do_action(1, SimpleAction(action_type=ActionType.CONTINUE))
        round.do_action(1, HandTileAction(action_type=ActionType.DISCARD, tile=21))
        assert round.discard_tiles == [10, 21]

    def test_closed_kan(self) -> None:
        round = Round(tiles=test_deck1)
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=10))
        round.do_action(1, SimpleAction(action_type=ActionType.DRAW))
        round.do_action(1, HandTileAction(action_type=ActionType.DISCARD, tile=21))
        round.do_action(2, SimpleAction(action_type=ActionType.DRAW))
        round.do_action(2, ClosedKanAction(tiles=(110, 111, 112, 113)))
        assert round.get_hand(2) == [
            22,
            130,
            131,
            132,
            133,
            150,
            151,
            152,
            153,
            172,
            83,
        ]
        assert round.get_calls(2) == [ClosedKanCall(tiles=(110, 111, 112, 113))]
        round.do_action(2, SimpleAction(action_type=ActionType.CONTINUE))
        round.do_action(2, HandTileAction(action_type=ActionType.DISCARD, tile=130))
        assert round.discard_tiles == [10, 21, 130]

    def test_deck_2_start_hands(self) -> None:
        round = Round(tiles=test_deck2)
        assert round.get_hand(0) == [
            10,
            11,
            12,
            13,
            40,
            41,
            42,
            43,
            70,
            71,
            72,
            91,
            130,
            360,
        ]
        assert round.get_calls(0) == []
        assert round.get_flowers(0) == [410, 430]
        assert round.get_hand(1) == [
            20,
            21,
            22,
            23,
            50,
            51,
            52,
            53,
            73,
            131,
            132,
            133,
            370,
        ]
        assert round.get_calls(1) == []
        assert round.get_flowers(1) == [420]
        assert round.get_hand(2) == [
            110,
            111,
            112,
            120,
            121,
            122,
            140,
            150,
            310,
            311,
            320,
            321,
            322,
        ]
        assert round.get_hand(3) == [30, 31, 32, 33, 60, 61, 62, 63, 80, 81, 82, 83, 90]

    def test_history(self) -> None:
        round = Round(tiles=test_deck1)
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=90))
        round.do_action(
            1, OpenCallAction(action_type=ActionType.PON, other_tiles=(91, 92))
        )
        round.do_action(1, HandTileAction(action_type=ActionType.DISCARD, tile=213))
        round.do_action(
            0, OpenCallAction(action_type=ActionType.PON, other_tiles=(210, 211))
        )
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=10))
        round.do_action(1, SimpleAction(action_type=ActionType.DRAW))
        round.do_action(
            1,
            AddKanAction(
                tile=93,
                pon_call=OpenCall(
                    call_type=CallType.PON,
                    called_player_index=0,
                    called_tile=90,
                    other_tiles=(91, 92),
                ),
            ),
        )
        round.do_action(1, SimpleAction(action_type=ActionType.CONTINUE))
        round.do_action(1, HandTileAction(action_type=ActionType.DISCARD, tile=21))
        assert round.history == [
            (0, SimpleAction(action_type=ActionType.CONTINUE)),
            (1, SimpleAction(action_type=ActionType.CONTINUE)),
            (2, SimpleAction(action_type=ActionType.CONTINUE)),
            (3, SimpleAction(action_type=ActionType.CONTINUE)),
            (0, SimpleAction(action_type=ActionType.CONTINUE)),
            (0, HandTileAction(action_type=ActionType.DISCARD, tile=90)),
            (1, OpenCallAction(action_type=ActionType.PON, other_tiles=(91, 92))),
            (1, HandTileAction(action_type=ActionType.DISCARD, tile=213)),
            (0, OpenCallAction(action_type=ActionType.PON, other_tiles=(210, 211))),
            (0, HandTileAction(action_type=ActionType.DISCARD, tile=10)),
            (1, SimpleAction(action_type=ActionType.DRAW)),
            (
                1,
                AddKanAction(
                    tile=93,
                    pon_call=OpenCall(
                        call_type=CallType.PON,
                        called_player_index=0,
                        called_tile=90,
                        other_tiles=(91, 92),
                    ),
                ),
            ),
            (1, SimpleAction(action_type=ActionType.CONTINUE)),
            (1, HandTileAction(action_type=ActionType.DISCARD, tile=21)),
        ]

    def test_ron(self) -> None:
        round = Round(tiles=test_deck2)
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=130))
        round.do_action(2, SimpleAction(action_type=ActionType.RON))
        assert round.status == RoundStatus.END
        win_info = round.win
        assert win_info is not None
        assert win_info.win_player == 2
        assert win_info.lose_player == 0
        assert win_info.hand == [
            110,
            111,
            112,
            120,
            121,
            122,
            140,
            150,
            310,
            311,
            320,
            321,
            322,
            130,
        ]
        assert win_info.calls == []

    def test_tsumo(self) -> None:
        round = Round(tiles=test_deck2)
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=10))
        round.do_action(1, SimpleAction(action_type=ActionType.DRAW))
        round.do_action(1, HandTileAction(action_type=ActionType.DISCARD, tile=20))
        round.do_action(2, SimpleAction(action_type=ActionType.DRAW))
        round.do_action(2, SimpleAction(action_type=ActionType.TSUMO))
        assert round.status == RoundStatus.END
        win_info = round.win
        assert win_info is not None
        assert win_info.win_player == 2
        assert win_info.lose_player is None
        assert win_info.hand == [
            110,
            111,
            112,
            120,
            121,
            122,
            140,
            150,
            310,
            311,
            320,
            321,
            322,
            160,
        ]
        assert win_info.calls == []

    def test_min_yaku_enough_yaku(self) -> None:
        round = Round(tiles=test_deck2, options=GameOptions(min_yaku=7))
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=130))
        # ronning here gives 7 yaku 1 dora
        assert (
            SimpleAction(action_type=ActionType.RON) in round.allowed_actions[2].actions
        )

    def test_min_yaku_not_enough_yaku(self) -> None:
        round = Round(tiles=test_deck2, options=GameOptions(min_yaku=8))
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=130))
        # ronning here gives 7 yaku 1 dora
        assert (
            SimpleAction(action_type=ActionType.RON)
            not in round.allowed_actions[2].actions
        )

    def test_chankan(self) -> None:
        round = Round(tiles=test_deck2)
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=130))
        round.do_action(
            1, OpenCallAction(action_type=ActionType.PON, other_tiles=(131, 132))
        )
        round.do_action(1, HandTileAction(action_type=ActionType.DISCARD, tile=73))
        round.do_action(2, SimpleAction(action_type=ActionType.DRAW))
        round.do_action(2, HandTileAction(action_type=ActionType.DISCARD, tile=92))
        round.do_action(3, SimpleAction(action_type=ActionType.DRAW))
        round.do_action(3, HandTileAction(action_type=ActionType.DISCARD, tile=30))
        round.do_action(0, SimpleAction(action_type=ActionType.DRAW))
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=10))
        round.do_action(1, SimpleAction(action_type=ActionType.DRAW))
        round.do_action(
            1,
            AddKanAction(
                tile=133,
                pon_call=OpenCall(
                    call_type=CallType.PON,
                    called_player_index=0,
                    called_tile=130,
                    other_tiles=(131, 132),
                ),
            ),
        )
        round.do_action(2, SimpleAction(action_type=ActionType.RON))
        assert round.status == RoundStatus.END
        win_info = round.win
        assert win_info is not None
        assert win_info.win_player == 2
        assert win_info.lose_player == 1
        assert win_info.hand == [
            110,
            111,
            112,
            120,
            121,
            122,
            140,
            150,
            310,
            311,
            320,
            321,
            322,
            133,
        ]
        assert win_info.calls == []
        assert win_info.is_chankan

    def test_auto_flower_history(self) -> None:
        round = Round(tiles=test_deck3, options=GameOptions(auto_replace_flowers=True))
        assert round.history == [
            (0, HandTileAction(action_type=ActionType.FLOWER, tile=410)),
            (0, HandTileAction(action_type=ActionType.FLOWER, tile=430)),
            (0, SimpleAction(action_type=ActionType.CONTINUE)),
            (1, HandTileAction(action_type=ActionType.FLOWER, tile=420)),
            (1, SimpleAction(action_type=ActionType.CONTINUE)),
            (2, SimpleAction(action_type=ActionType.CONTINUE)),
            (3, SimpleAction(action_type=ActionType.CONTINUE)),
            (0, HandTileAction(action_type=ActionType.FLOWER, tile=440)),
            (0, SimpleAction(action_type=ActionType.CONTINUE)),
            (1, SimpleAction(action_type=ActionType.CONTINUE)),
            (2, SimpleAction(action_type=ActionType.CONTINUE)),
            (3, SimpleAction(action_type=ActionType.CONTINUE)),
            (0, SimpleAction(action_type=ActionType.CONTINUE)),
        ]

    def test_sub_round_auto_flower_history(self) -> None:
        round = Round(
            tiles=test_deck3,
            sub_round=1,
            options=GameOptions(auto_replace_flowers=True),
        )
        assert round.history == [
            (1, HandTileAction(action_type=ActionType.FLOWER, tile=410)),
            (1, HandTileAction(action_type=ActionType.FLOWER, tile=430)),
            (1, SimpleAction(action_type=ActionType.CONTINUE)),
            (2, HandTileAction(action_type=ActionType.FLOWER, tile=420)),
            (2, SimpleAction(action_type=ActionType.CONTINUE)),
            (3, SimpleAction(action_type=ActionType.CONTINUE)),
            (0, SimpleAction(action_type=ActionType.CONTINUE)),
            (1, HandTileAction(action_type=ActionType.FLOWER, tile=440)),
            (1, SimpleAction(action_type=ActionType.CONTINUE)),
            (2, SimpleAction(action_type=ActionType.CONTINUE)),
            (3, SimpleAction(action_type=ActionType.CONTINUE)),
            (0, SimpleAction(action_type=ActionType.CONTINUE)),
            (1, SimpleAction(action_type=ActionType.CONTINUE)),
        ]

    def test_auto_flower_one_person_draw_flower(self) -> None:
        round = Round(tiles=test_deck5, options=GameOptions(auto_replace_flowers=True))
        assert round.history == [
            (0, HandTileAction(action_type=ActionType.FLOWER, tile=410)),
            (0, SimpleAction(action_type=ActionType.CONTINUE)),
            (1, SimpleAction(action_type=ActionType.CONTINUE)),
            (2, SimpleAction(action_type=ActionType.CONTINUE)),
            (3, SimpleAction(action_type=ActionType.CONTINUE)),
            (0, HandTileAction(action_type=ActionType.FLOWER, tile=420)),
            (0, SimpleAction(action_type=ActionType.CONTINUE)),
            (1, SimpleAction(action_type=ActionType.CONTINUE)),
            (2, SimpleAction(action_type=ActionType.CONTINUE)),
            (3, SimpleAction(action_type=ActionType.CONTINUE)),
            (0, SimpleAction(action_type=ActionType.CONTINUE)),
        ]

    def test_manual_flower_start(self) -> None:
        round = Round(tiles=test_deck3, options=GameOptions(auto_replace_flowers=False))
        assert round.status == RoundStatus.START

    def test_start_flower_call(self) -> None:
        round = Round(tiles=test_deck3, options=GameOptions(auto_replace_flowers=False))
        round.do_action(0, HandTileAction(action_type=ActionType.FLOWER, tile=410))
        assert round.get_flowers(0) == [410]

    def test_start_flower_calls(self) -> None:
        round = Round(tiles=test_deck3, options=GameOptions(auto_replace_flowers=False))
        round.do_action(0, HandTileAction(action_type=ActionType.FLOWER, tile=410))
        round.do_action(0, HandTileAction(action_type=ActionType.FLOWER, tile=430))
        round.do_action(0, HandTileAction(action_type=ActionType.FLOWER, tile=440))
        assert round.get_flowers(0) == [410, 430, 440]

    def test_start_flower_next_player(self) -> None:
        round = Round(tiles=test_deck3, options=GameOptions(auto_replace_flowers=False))
        round.do_action(0, HandTileAction(action_type=ActionType.FLOWER, tile=410))
        round.do_action(0, HandTileAction(action_type=ActionType.FLOWER, tile=430))
        round.do_action(0, HandTileAction(action_type=ActionType.FLOWER, tile=440))
        round.do_action(0, SimpleAction(action_type=ActionType.CONTINUE))
        round.do_action(1, HandTileAction(action_type=ActionType.FLOWER, tile=420))
        assert round.get_hand(1) == [
            20,
            21,
            22,
            23,
            60,
            61,
            62,
            63,
            120,
            121,
            122,
            123,
            350,
        ]
        assert round.get_flowers(1) == [420]

    def test_start_flower_pass_all(self) -> None:
        round = Round(tiles=test_deck3, options=GameOptions(auto_replace_flowers=False))
        round.do_action(0, HandTileAction(action_type=ActionType.FLOWER, tile=410))
        round.do_action(0, HandTileAction(action_type=ActionType.FLOWER, tile=430))
        round.do_action(0, HandTileAction(action_type=ActionType.FLOWER, tile=440))
        round.do_action(0, SimpleAction(action_type=ActionType.CONTINUE))
        round.do_action(1, HandTileAction(action_type=ActionType.FLOWER, tile=420))
        round.do_action(1, SimpleAction(action_type=ActionType.CONTINUE))
        round.do_action(2, SimpleAction(action_type=ActionType.CONTINUE))
        round.do_action(3, SimpleAction(action_type=ActionType.CONTINUE))
        round.do_action(0, SimpleAction(action_type=ActionType.CONTINUE))
        round.do_action(1, SimpleAction(action_type=ActionType.CONTINUE))
        assert round.current_player == 0
        assert round.status == RoundStatus.PLAY

    def test_start_flower_loop_pass_all(self) -> None:
        round = Round(tiles=test_deck3, options=GameOptions(auto_replace_flowers=False))
        round.do_action(0, HandTileAction(action_type=ActionType.FLOWER, tile=410))
        round.do_action(0, HandTileAction(action_type=ActionType.FLOWER, tile=430))
        round.do_action(0, SimpleAction(action_type=ActionType.CONTINUE))
        round.do_action(1, HandTileAction(action_type=ActionType.FLOWER, tile=420))
        round.do_action(1, SimpleAction(action_type=ActionType.CONTINUE))
        round.do_action(2, SimpleAction(action_type=ActionType.CONTINUE))
        round.do_action(3, SimpleAction(action_type=ActionType.CONTINUE))
        round.do_action(0, HandTileAction(action_type=ActionType.FLOWER, tile=440))
        round.do_action(0, SimpleAction(action_type=ActionType.CONTINUE))
        round.do_action(1, SimpleAction(action_type=ActionType.CONTINUE))
        round.do_action(2, SimpleAction(action_type=ActionType.CONTINUE))
        round.do_action(3, SimpleAction(action_type=ActionType.CONTINUE))
        round.do_action(0, SimpleAction(action_type=ActionType.CONTINUE))
        assert round.current_player == 0
        assert round.status == RoundStatus.PLAY

    def test_draw_flower(self) -> None:
        round = Round(tiles=test_deck3, options=GameOptions(auto_replace_flowers=False))
        round.do_action(0, HandTileAction(action_type=ActionType.FLOWER, tile=410))
        round.do_action(0, HandTileAction(action_type=ActionType.FLOWER, tile=430))
        round.do_action(0, SimpleAction(action_type=ActionType.CONTINUE))
        round.do_action(1, HandTileAction(action_type=ActionType.FLOWER, tile=420))
        round.do_action(1, SimpleAction(action_type=ActionType.CONTINUE))
        round.do_action(2, SimpleAction(action_type=ActionType.CONTINUE))
        round.do_action(3, SimpleAction(action_type=ActionType.CONTINUE))
        round.do_action(0, HandTileAction(action_type=ActionType.FLOWER, tile=440))
        round.do_action(0, SimpleAction(action_type=ActionType.CONTINUE))
        round.do_action(1, SimpleAction(action_type=ActionType.CONTINUE))
        round.do_action(2, SimpleAction(action_type=ActionType.CONTINUE))
        round.do_action(3, SimpleAction(action_type=ActionType.CONTINUE))
        round.do_action(0, SimpleAction(action_type=ActionType.CONTINUE))
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=10))
        round.do_action(1, SimpleAction(action_type=ActionType.DRAW))
        round.do_action(1, HandTileAction(action_type=ActionType.DISCARD, tile=20))
        round.do_action(2, SimpleAction(action_type=ActionType.DRAW))
        round.do_action(2, HandTileAction(action_type=ActionType.FLOWER, tile=450))
        assert round.get_flowers(2) == [450]
        assert round.get_hand(2) == [
            30,
            31,
            32,
            33,
            70,
            71,
            72,
            73,
            90,
            130,
            131,
            132,
            133,
            460,
        ]

    def test_priority(self) -> None:
        round = Round(tiles=test_deck4)
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=130))
        actions: list[Action | None] = [
            SimpleAction(action_type=ActionType.PASS),
            OpenCallAction(action_type=ActionType.CHII, other_tiles=(110, 120)),
            OpenCallAction(action_type=ActionType.PON, other_tiles=(131, 132)),
            SimpleAction(action_type=ActionType.RON),
        ]
        playeraction = round.get_priority_action(actions)
        assert playeraction is not None
        player, action = playeraction
        assert player == 3
        assert action == SimpleAction(action_type=ActionType.RON)

    def test_priority_with_none(self) -> None:
        round = Round(tiles=test_deck4)
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=130))
        actions: list[Action | None] = [
            None,
            OpenCallAction(action_type=ActionType.CHII, other_tiles=(110, 120)),
            OpenCallAction(action_type=ActionType.PON, other_tiles=(131, 132)),
            SimpleAction(action_type=ActionType.RON),
        ]
        playeraction = round.get_priority_action(actions)
        assert playeraction is not None
        player, action = playeraction
        assert player == 3
        assert action == SimpleAction(action_type=ActionType.RON)

    def test_priority_strong_call_and_none(self) -> None:
        round = Round(tiles=test_deck4)
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=130))
        actions: list[Action | None] = [
            None,
            None,
            None,
            SimpleAction(action_type=ActionType.RON),
        ]
        playeraction = round.get_priority_action(actions)
        assert playeraction is not None
        player, action = playeraction
        assert player == 3
        assert action == SimpleAction(action_type=ActionType.RON)

    def test_priority_weak_call_and_none(self) -> None:
        round = Round(tiles=test_deck4)
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=130))
        actions: list[Action | None] = [
            None,
            OpenCallAction(action_type=ActionType.CHII, other_tiles=(110, 120)),
            None,
            None,
        ]
        playeraction = round.get_priority_action(actions)
        assert playeraction is None

    def test_priority_no_choice_all_none(self) -> None:
        round = Round(tiles=test_deck4)
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=10))
        actions: list[Action | None] = [
            None,
            None,
            None,
            None,
        ]
        playeraction = round.get_priority_action(actions)
        assert playeraction is not None
        player, action = playeraction
        assert player == 1
        assert action == SimpleAction(action_type=ActionType.DRAW)

    def test_priority_bad_action(self) -> None:
        round = Round(tiles=test_deck4)
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=130))
        actions: list[Action | None] = [
            SimpleAction(action_type=ActionType.PASS),
            OpenCallAction(action_type=ActionType.CHII, other_tiles=(110, 120)),
            SimpleAction(action_type=ActionType.RON),
            SimpleAction(action_type=ActionType.PASS),
        ]
        playeraction = round.get_priority_action(actions)
        assert playeraction is not None
        player, action = playeraction
        assert player == 1
        assert action == OpenCallAction(
            action_type=ActionType.CHII, other_tiles=(110, 120)
        )

    def test_priority_bad_action_and_none(self) -> None:
        round = Round(tiles=test_deck4)
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=130))
        actions: list[Action | None] = [
            None,
            OpenCallAction(action_type=ActionType.CHII, other_tiles=(110, 120)),
            OpenCallAction(action_type=ActionType.PON, other_tiles=(131, 132)),
            OpenKanAction(other_tiles=(131, 132, 133)),
        ]
        playeraction = round.get_priority_action(actions)
        assert playeraction is not None
        player, action = playeraction
        assert player == 2
        assert action == OpenCallAction(
            action_type=ActionType.PON, other_tiles=(131, 132)
        )

    def test_priority_current_player(self) -> None:
        round = Round(tiles=test_deck4)
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=130))
        round.do_action(1, SimpleAction(action_type=ActionType.DRAW))
        round.do_action(1, ClosedKanAction(tiles=(50, 51, 52, 53)))
        actions: list[Action | None] = [
            SimpleAction(action_type=ActionType.PASS),
            SimpleAction(action_type=ActionType.CONTINUE),
            SimpleAction(action_type=ActionType.PASS),
            SimpleAction(action_type=ActionType.PASS),
        ]
        playeraction = round.get_priority_action(actions)
        assert playeraction is not None
        player, action = playeraction
        assert player == 1
        assert action == SimpleAction(action_type=ActionType.CONTINUE)

    def test_use_all_tiles(self) -> None:
        round = Round(
            tiles=test_deck4,
            options=GameOptions(
                max_dora_count=0, start_dora_count=0, dead_wall_additional_tiles=2
            ),
        )
        while round.status != RoundStatus.END:
            actions = [action_set.default for action_set in round.allowed_actions]
            playeraction = round.get_priority_action(actions)
            assert playeraction is not None
            player, action = playeraction
            round.do_action(player, action)
        assert round.wall_count == 14
        assert round.win is None

    def test_haitei(self) -> None:
        round = Round(
            tiles=test_deck_haitei,
            options=GameOptions(
                max_dora_count=0, start_dora_count=0, dead_wall_additional_tiles=2
            ),
        )
        while round.wall_count > 14:
            actions = [action_set.default for action_set in round.allowed_actions]
            playeraction = round.get_priority_action(actions)
            assert playeraction is not None
            player, action = playeraction
            round.do_action(player, action)
        assert round.current_player == 1
        assert round.status == RoundStatus.PLAY
        round.do_action(1, SimpleAction(action_type=ActionType.TSUMO))
        assert round.win is not None
        assert round.win.is_haitei

    def test_houtei(self) -> None:
        round = Round(
            tiles=test_deck4,
            options=GameOptions(
                max_dora_count=0, start_dora_count=0, dead_wall_additional_tiles=2
            ),
        )
        round.do_action(0, ClosedKanAction(tiles=(40, 41, 42, 43)))
        while round.wall_count > 14:
            actions = [action_set.default for action_set in round.allowed_actions]
            playeraction = round.get_priority_action(actions)
            assert playeraction is not None
            player, action = playeraction
            round.do_action(player, action)
        assert round.current_player == 0
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=130))
        assert round.status == RoundStatus.LAST_DISCARDED
        round.do_action(3, SimpleAction(action_type=ActionType.RON))
        assert round.win is not None
        assert round.win.is_houtei

    def test_after_flower(self) -> None:
        round = Round(tiles=test_deck_rinshan1)
        round.do_action(0, SimpleAction(action_type=ActionType.TSUMO))
        win_info = round.win
        assert win_info is not None
        assert win_info.after_flower_count == 5

    def test_after_flower_and_closed_kan(self) -> None:
        round = Round(tiles=test_deck_rinshan1)
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=110))
        round.do_action(1, SimpleAction(action_type=ActionType.DRAW))
        round.do_action(1, ClosedKanAction(tiles=(10, 11, 12, 13)))
        round.do_action(1, SimpleAction(action_type=ActionType.CONTINUE))
        round.do_action(1, HandTileAction(action_type=ActionType.FLOWER, tile=480))
        round.do_action(1, SimpleAction(action_type=ActionType.TSUMO))
        win_info = round.win
        assert win_info is not None
        assert win_info.after_flower_count == 1
        assert win_info.after_kan_count == 1

    def test_after_flower_and_open_kan(self) -> None:
        round = Round(tiles=test_deck_rinshan2)
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=10))
        round.do_action(1, OpenKanAction(other_tiles=(11, 12, 13)))
        round.do_action(1, HandTileAction(action_type=ActionType.FLOWER, tile=480))
        round.do_action(1, SimpleAction(action_type=ActionType.TSUMO))
        win_info = round.win
        assert win_info is not None
        assert win_info.after_flower_count == 1
        assert win_info.after_kan_count == 1

    def test_tenhou(self) -> None:
        round = Round(tiles=test_deck_kan_tenhou)
        round.do_action(0, SimpleAction(action_type=ActionType.TSUMO))
        assert round.win is not None
        assert round.win.is_tenhou

    def test_sub_round_tenhou(self) -> None:
        round = Round(tiles=test_deck_kan_tenhou, sub_round=1)
        round.do_action(1, SimpleAction(action_type=ActionType.TSUMO))
        assert round.win is not None
        assert round.win.is_tenhou

    def test_not_tenhou_after_call(self) -> None:
        round = Round(tiles=test_deck_kan_tenhou)
        round.do_action(0, ClosedKanAction(tiles=(160, 161, 162, 163)))
        round.do_action(0, SimpleAction(action_type=ActionType.CONTINUE))
        round.do_action(0, SimpleAction(action_type=ActionType.TSUMO))
        assert round.win is not None
        assert not round.win.is_tenhou

    def test_chiihou(self) -> None:
        round = Round(tiles=test_deck_kan_tenhou)
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=110))
        round.do_action(1, SimpleAction(action_type=ActionType.DRAW))
        round.do_action(1, SimpleAction(action_type=ActionType.TSUMO))
        assert round.win is not None
        assert round.win.is_chiihou

    def test_not_chiihou_after_call(self) -> None:
        round = Round(tiles=test_deck_kan_tenhou)
        round.do_action(0, ClosedKanAction(tiles=(160, 161, 162, 163)))
        round.do_action(0, SimpleAction(action_type=ActionType.CONTINUE))
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=110))
        round.do_action(1, SimpleAction(action_type=ActionType.DRAW))
        round.do_action(1, SimpleAction(action_type=ActionType.TSUMO))
        assert round.win is not None
        assert not round.win.is_chiihou
