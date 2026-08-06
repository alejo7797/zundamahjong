import unittest

from tests.decks import test_deck1
from zundamahjong.mahjong.deck import Deck


class DoraTest(unittest.TestCase):
    def test_dora_indicators(self) -> None:
        deck = Deck(tiles=test_deck1, max_back_draw=12, max_dora_count=5)
        self.assertSequenceEqual(deck.dora, [330, 322, 320, 312, 310])
        self.assertSequenceEqual(deck.ura_dora, [331, 323, 321, 313, 311])
