import unittest

from tests.decks import test_deck1
from zundamahjong.mahjong.action import (
    ActionType,
    AddKanAction,
    HandTileAction,
    OpenCallAction,
    SimpleAction,
)
from zundamahjong.mahjong.bot import unseen_frequencies
from zundamahjong.mahjong.call import CallType, OpenCall
from zundamahjong.mahjong.game import Game


class BotTest(unittest.TestCase):
    def test_unseen_freqs(self) -> None:
        game = Game(first_deck_tiles=test_deck1)
        round = game.round
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=170))
        info = game.info(0)
        freqs = unseen_frequencies(info)
        self.assertDictEqual(
            freqs,
            {
                1: 2,
                2: 3,
                3: 3,
                4: 3,
                5: 3,
                6: 3,
                7: 3,
                8: 3,
                9: 3,
                11: 4,
                12: 4,
                13: 4,
                14: 4,
                15: 4,
                16: 4,
                17: 3,
                18: 4,
                19: 4,
                21: 1,
                22: 4,
                23: 4,
                24: 4,
                25: 4,
                26: 4,
                27: 4,
                28: 4,
                29: 4,
                31: 4,
                32: 4,
                33: 4,
                34: 4,
                35: 4,
                36: 4,
                37: 4,
            },
        )

    def test_unseen_freqs_call(self) -> None:
        game = Game(first_deck_tiles=test_deck1)
        round = game.round
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=50))
        round.do_action(
            1,
            OpenCallAction(action_type=ActionType.CHII, other_tiles=(61, 71)),
        )
        info = game.info(0)
        freqs = unseen_frequencies(info)
        self.assertDictEqual(
            freqs,
            {
                1: 2,
                2: 3,
                3: 3,
                4: 3,
                5: 3,
                6: 2,
                7: 2,
                8: 3,
                9: 3,
                11: 4,
                12: 4,
                13: 4,
                14: 4,
                15: 4,
                16: 4,
                17: 3,
                18: 4,
                19: 4,
                21: 1,
                22: 4,
                23: 4,
                24: 4,
                25: 4,
                26: 4,
                27: 4,
                28: 4,
                29: 4,
                31: 4,
                32: 4,
                33: 4,
                34: 4,
                35: 4,
                36: 4,
                37: 4,
            },
        )

    def test_unseen_freqs_add_kan(self) -> None:
        game = Game(first_deck_tiles=test_deck1)
        round = game.round
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
        info = game.info(0)
        freqs = unseen_frequencies(info)
        self.assertDictEqual(
            freqs,
            {
                1: 2,
                2: 3,
                3: 3,
                4: 3,
                5: 3,
                6: 3,
                7: 3,
                8: 3,
                9: 0,
                11: 4,
                12: 4,
                13: 4,
                14: 4,
                15: 4,
                16: 4,
                17: 3,
                18: 4,
                19: 4,
                21: 0,
                22: 4,
                23: 4,
                24: 4,
                25: 4,
                26: 4,
                27: 4,
                28: 4,
                29: 4,
                31: 4,
                32: 4,
                33: 4,
                34: 4,
                35: 4,
                36: 4,
                37: 4,
            },
        )
