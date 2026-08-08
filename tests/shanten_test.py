import unittest

from zundamahjong.mahjong.shanten import (
    calculate_shanten,
    honours_shanten_data,
    suit_shanten_data,
)


class ShantenTest(unittest.TestCase):
    def test_honours_shanten_1(self) -> None:
        data = honours_shanten_data([1, 0, 0, 0, 0, 0, 0])
        assert data == [
            [0, 0],
            [1, 64],
            [1, 64],
            [1, 127],
            [1, 127],
            [1, 127],
            [1, 127],
            [1, 127],
            [1, 127],
            [1, 127],
        ]

    def test_honours_shanten_112(self) -> None:
        data = honours_shanten_data([2, 1, 0, 0, 0, 0, 0])
        assert data == [
            [0, 0],
            [2, 0],
            [2, 64],
            [3, 96],
            [3, 96],
            [3, 127],
            [3, 127],
            [3, 127],
            [3, 127],
            [3, 127],
        ]

    def test_honours_shanten_11123(self) -> None:
        data = honours_shanten_data([3, 1, 1, 0, 0, 0, 0])
        assert data == [
            [0, 0],
            [2, 0],
            [3, 0],
            [4, 48],
            [4, 48],
            [5, 48],
            [5, 48],
            [5, 127],
            [5, 127],
            [5, 127],
        ]

    def test_honours_shanten_112234(self) -> None:
        data = honours_shanten_data([2, 2, 1, 1, 0, 0, 0])
        assert data == [
            [0, 0],
            [2, 0],
            [2, 96],
            [4, 96],
            [4, 96],
            [5, 120],
            [5, 120],
            [6, 120],
            [6, 120],
            [6, 127],
        ]

    def test_honours_shanten_11112234(self) -> None:
        data = honours_shanten_data([4, 2, 1, 1, 0, 0, 0])
        assert data == [
            [0, 0],
            [2, 0],
            [3, 0],
            [5, 0],
            [5, 32],
            [6, 120],
            [6, 120],
            [7, 120],
            [7, 120],
            [8, 120],
        ]

    def test_suit_shanten_1(self) -> None:
        data = suit_shanten_data([1, 0, 0, 0, 0, 0, 0, 0, 0])
        assert data == [
            [0, 0],
            [1, 256],
            [1, 448],
            [1, 511],
            [1, 511],
            [1, 511],
            [1, 511],
            [1, 511],
            [1, 511],
            [1, 511],
        ]

    def test_suit_shanten_5(self) -> None:
        data = suit_shanten_data([0, 0, 0, 0, 1, 0, 0, 0, 0])
        assert data == [
            [0, 0],
            [1, 16],
            [1, 124],
            [1, 511],
            [1, 511],
            [1, 511],
            [1, 511],
            [1, 511],
            [1, 511],
            [1, 511],
        ]

    def test_suit_shanten_34(self) -> None:
        data = suit_shanten_data([0, 0, 1, 1, 0, 0, 0, 0, 0])
        assert data == [
            [0, 0],
            [1, 96],
            [2, 144],
            [2, 511],
            [2, 511],
            [2, 511],
            [2, 511],
            [2, 511],
            [2, 511],
            [2, 511],
        ]

    def test_suit_shanten_2344(self) -> None:
        data = suit_shanten_data([0, 1, 1, 2, 0, 0, 0, 0, 0])
        assert data == [
            [0, 0],
            [2, 0],
            [3, 0],
            [4, 288],
            [4, 504],
            [4, 511],
            [4, 511],
            [4, 511],
            [4, 511],
            [4, 511],
        ]

    def test_suit_shanten_233444556(self) -> None:
        data = suit_shanten_data([0, 1, 2, 3, 2, 1, 0, 0, 0])
        assert data == [
            [0, 0],
            [2, 0],
            [3, 0],
            [5, 0],
            [6, 0],
            [7, 508],
            [9, 0],
            [9, 511],
            [9, 511],
            [9, 511],
        ]

    def test_shanten_1shanten_small(self) -> None:
        shanten, useful_tiles = calculate_shanten([2, 3, 15, 32])
        assert shanten == 1
        assert useful_tiles == {1, 4, 15, 32}

    def test_shanten_1shanten(self) -> None:
        shanten, useful_tiles = calculate_shanten(
            [5, 6, 7, 8, 9, 17, 18, 19, 23, 24, 29, 29, 29]
        )
        assert shanten == 1
        assert useful_tiles == {4, 5, 6, 7, 8, 9, 22, 23, 24, 25}

    def test_shanten_2shanten(self) -> None:
        shanten, useful_tiles = calculate_shanten(
            [7, 8, 12, 14, 18, 18, 23, 24, 24, 26, 27, 27, 28]
        )
        assert shanten == 2
        assert useful_tiles == {6, 9, 13, 18, 22, 24, 25}

    def test_shanten_2shanten_allow7pairs(self) -> None:
        shanten, useful_tiles = calculate_shanten(
            [3, 4, 4, 11, 12, 13, 17, 17, 24, 26, 26, 35, 35]
        )
        assert shanten == 2
        assert useful_tiles == {2, 3, 4, 5, 11, 12, 13, 17, 24, 25, 26, 35}

    def test_shanten_3shanten(self) -> None:
        shanten, useful_tiles = calculate_shanten(
            [14, 17, 18, 22, 24, 25, 26, 27, 28, 33, 35, 37, 37]
        )
        assert shanten == 3
        assert useful_tiles == {
            12,
            13,
            14,
            15,
            16,
            19,
            21,
            22,
            23,
            24,
            25,
            26,
            27,
            28,
            29,
            33,
            35,
            37,
        }

    def test_shanten_4shanten_allow7pairs_allow13orphans(self) -> None:
        shanten, useful_tiles = calculate_shanten(
            [1, 9, 11, 19, 21, 23, 31, 31, 31, 31, 32, 32, 33]
        )
        assert shanten == 4
        assert useful_tiles == {
            1,
            2,
            3,
            7,
            8,
            9,
            11,
            12,
            13,
            17,
            18,
            19,
            21,
            22,
            23,
            29,
            31,
            32,
            33,
            34,
            35,
            36,
            37,
        }

    def test_shanten_3player(self) -> None:
        shanten, useful_tiles = calculate_shanten([1, 9, 25, 25], is_3player=True)
        assert shanten == 1
        assert useful_tiles == {1, 9, 25}
