import unittest

from tests.decks import test_deck1
from zundamahjong.mahjong.action import (
    ActionType,
    AddKanAction,
    ClosedKanAction,
    HandTileAction,
    OpenCallAction,
    OpenKanAction,
    SimpleAction,
)
from zundamahjong.mahjong.call import CallType, OpenCall
from zundamahjong.mahjong.deck import Deck
from zundamahjong.mahjong.game_options import GameOptions
from zundamahjong.mahjong.round import Round


class DoraTest(unittest.TestCase):
    def test_deck_dora_indicators(self) -> None:
        deck = Deck(tiles=test_deck1, max_back_draw=12, max_dora_count=5)
        assert deck.dora == (330, 322, 320, 312, 310)
        assert deck.ura_dora == (331, 323, 321, 313, 311)

    def test_dora_indicators(self) -> None:
        round = Round(
            tiles=test_deck1,
            options=GameOptions(max_kan_count=4, max_dora_count=5, start_dora_count=1),
        )
        assert round.dora == [330]
        assert round.ura_dora == [331]

    def test_open_kan_kan_count(self) -> None:
        round = Round(
            tiles=test_deck1,
            options=GameOptions(max_kan_count=4, max_dora_count=5, start_dora_count=1),
        )
        assert round.kan_count == 0
        assert round.dora == [330]
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=10))
        round.do_action(1, SimpleAction(action_type=ActionType.DRAW))
        round.do_action(1, HandTileAction(action_type=ActionType.DISCARD, tile=213))
        round.do_action(0, OpenKanAction(other_tiles=(210, 211, 212)))
        assert round.kan_count == 1
        assert round.dora == [330, 322]
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=20))
        assert round.kan_count == 1
        assert round.dora == [330, 322]

    def test_add_kan_kan_count(self) -> None:
        round = Round(
            tiles=test_deck1,
            options=GameOptions(max_kan_count=4, max_dora_count=5, start_dora_count=1),
        )
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
        assert round.kan_count == 0
        assert round.dora == [330]
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
        assert round.kan_count == 1
        assert round.dora == [330, 322]
        round.do_action(1, SimpleAction(action_type=ActionType.CONTINUE))
        assert round.kan_count == 1
        assert round.dora == [330, 322]
        round.do_action(1, HandTileAction(action_type=ActionType.DISCARD, tile=21))
        assert round.kan_count == 1
        assert round.dora == [330, 322]

    def test_closed_kan_kan_count(self) -> None:
        round = Round(
            tiles=test_deck1,
            options=GameOptions(max_kan_count=4, max_dora_count=5, start_dora_count=1),
        )
        assert round.kan_count == 0
        assert round.dora == [330]
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=10))
        round.do_action(1, SimpleAction(action_type=ActionType.DRAW))
        round.do_action(1, HandTileAction(action_type=ActionType.DISCARD, tile=21))
        round.do_action(2, SimpleAction(action_type=ActionType.DRAW))
        assert round.kan_count == 0
        assert round.dora == [330]
        round.do_action(2, ClosedKanAction(tiles=(110, 111, 112, 113)))
        assert round.kan_count == 1
        assert round.dora == [330, 322]
        round.do_action(2, SimpleAction(action_type=ActionType.CONTINUE))
        round.do_action(2, HandTileAction(action_type=ActionType.DISCARD, tile=130))
        assert round.kan_count == 1
        assert round.dora == [330, 322]
