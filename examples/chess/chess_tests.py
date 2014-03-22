from oktest import ok

from chess_base import to_str_pos, to_tuple_pos, is_valid_cell, get_all_scales
from chess import Pawn, Rook, Knight, King, Queen, Bishop, Board

def test_pos_transform():
    pos_pairs = [((0, 0), "A1"),
                 ((7, 0), "H1"),
                 ((0, 7), "A8"),
                 ((7, 7), "H8"),
                 ((3, 4), "D5")]

    for tupl, sp in pos_pairs:
        ok(to_tuple_pos(sp)) == tupl
        ok(to_str_pos(tupl)) == sp

    for x in range(8):
        for y in range(8):
            ok(to_tuple_pos(to_str_pos((x, y)))) == (x, y)

def test_is_valid_poses():
    for x in range(8):
        for y in range(8):
            ok(is_valid_cell((x, y))).is_truthy()

    for x in (-200, 1.42, "as", -1, 8, 9, 100):
        for y in range(8):
            ok(is_valid_cell((x, y))).is_falsy()

    for y in (-200, 1.42, "as", -1, 8, 9, 100):
        for x in range(8):
            ok(is_valid_cell((x, y))).is_falsy()

    for y in (-200, 1.42, "as", -1, 8, 9, 100):
        for x in (-200, 1.42, "as", -1, 8, 9, 100):    
            ok(is_valid_cell((x, y))).is_falsy()


def test_get_all_scales():
    sc = [i for i in get_all_scales((0, 0), Rook.vects) if i != []]
    ok(sc).length(2)
    s1, s2 = sc
    
    ok(min(s1[0][0], s2[0][0])) == 0

    if s1[0][0] != 0:
        s1, s2 = s2, s1

    ok(set(s1)) == {(0, i) for i in range(1, 8)}
    ok(set(s2)) == {(i, 0) for i in range(1, 8)}

    sc = [i for i in get_all_scales((0, 0), Bishop.vects) if i != []]
    ok(sc).length(1)
    ok(set(sc[0])) == {(i, i) for i in range(1, 8)}

    for pos in [(3, 4), (0, 0), (2, 3), (7, 7), (0, 7)]:
        for color in "BW":
            for piece_cl in (Rook, Queen, Bishop):
                pmc1 = get_all_scales(pos, piece_cl.vects)
                pmc2 = piece_cl(pos, color).move_cells()
                pmc1.sort()
                pmc2.sort()

                ok(pmc1) == pmc2


def to_comparable_v(v2d):
    res = []
    for subvec in v2d:
        if subvec != []:
            ok(isinstance(subvec[0], tuple)).is_truthy()
            tmp = tuple()
            for i in subvec:
                tmp = tmp + i
            res.append(tmp)
    res.sort()
    return res


def text_pawn():
    p = Pawn((3, 3), "W")
    ok(p.move_cells()) == [[(3, 4)]]
    ok(to_comparable_v(p.hit_cells())) == [(2, 4), (4, 4)]

    p = Pawn((3, 4), "W")
    ok(p.move_cells()) == [[(3, 5)]]
    ok(to_comparable_v(p.hit_cells())) == [(2, 5), (4, 5)]

    p = Pawn((3, 4), "B")
    ok(p.move_cells()) == [[(3, 3)]]
    ok(to_comparable_v(p.hit_cells())) == [(2, 3), (4, 3)]

    p = Pawn((0, 4), "W")
    ok(p.move_cells()) == [[(0, 5)]]
    ok(p.hit_cells()) == [[(1, 5)]]

    p = Pawn((1, 7), "W")
    ok(p.move_cells()) == []
    ok(p.hit_cells()) == []

    p = Pawn((2, 1), "W")
    ok(p.move_cells()) == [[(2, 2), (2, 3)]]

    p = Pawn((2, 1), "B")
    ok(p.move_cells()) == [[(2, 0)]]

    p = Pawn((2, 6), "B")
    ok(p.move_cells()) == [[(2, 4), (2, 5)]]

