import unittest
from collections import Counter

from tests.decks import test_deck1, test_deck2, test_deck3, test_deck4, test_deck5
from zundamahjong.mahjong.deck import four_player_deck, four_player_flowers


class DeckTest(unittest.TestCase):
    def test_deck_sizes(self) -> None:
        for test_deck in [test_deck1, test_deck2, test_deck3, test_deck4, test_deck5]:
            assert Counter(test_deck) == Counter(four_player_deck + four_player_flowers)
