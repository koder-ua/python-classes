import time
from abc import abstractmethod


from chess_base import board_letters, to_str_pos, to_tuple_pos, get_all_scales
from chess_base import is_valid_cell, rev_color, color_index, color_sig


try:
    profile # if run under kernel_prof.py
except NameError:
    def profile(f):
        return f


class ChessPiece(object):
    name = None
    def_cost = None

    precached_moves = {}
    precached_hits = {}

    def __init__(self, pos, color):
        self.pos = to_tuple_pos(pos)
        self.color = color
        self.cost = color_sig[self.color] * self.def_cost

    def move(self, pos):
        self.pos = to_tuple_pos(pos)

    @abstractmethod
    def get_move_cells(self):
        pass

    def get_hit_cells(self):
        return self.get_move_cells()

    def hit_cells(self):
        return self.move_cells()

    def move_cells(self):
        eid = self.eq_id()
        res = self.precached_moves.get(eid)
        if res is None:
            res = self.get_move_cells()
            self.precached_moves[eid] = res
        return res

    def eq_id(self):
        return (self.name, self.pos)

    def full_name(self):
        return self.color + self.name

    def __str__(self):
        return "{}({!r}, {!r})".format(self.__class__.__name__, self.pos, self.color)

    def __repr__(self):
        return str(self)


class Pawn(ChessPiece):
    name = "P"
    def_cost = 1

    def eq_id(self):
        return (self.name, self.pos, self.color)

    def get_move_cells(self):
        x, y = self.pos
        if self.color == "W":
            new_positions = [(x, y + 1)]
            if y == 1:
                new_positions.append((x, y + 2))
        else:
            new_positions = [(x, y - 1)]
            if y == 6:
                new_positions.append((x, y - 2))
            
        return [filter(is_valid_cell, new_positions)]

    def get_hit_cells(self):
        x, y = self.pos
        if self.color == "W":
            new_positions = [(x + 1, y + 1), (x - 1, y + 1)]
        else:
            new_positions = [(x + 1, y - 1), (x - 1, y - 1)]
        return [[i] for i in new_positions if is_valid_cell(i)]

    def hit_cells(self):
        eid = self.eq_id()
        res = self.precached_hits.get(eid)
        if res is None:
            res = self.get_hit_cells()
            self.precached_hits[eid] = res
        return res


class Knight(ChessPiece):
    name = "N"
    def_cost = 3

    def get_move_cells(self):
        x, y = self.pos
        for dx in (-2, -1, 1, 2):
            for dy in (3 - abs(dx), -3 + abs(dx)):
                np = (x + dx, y + dy)
                if is_valid_cell(np):
                    yield [np]


class Bishop(ChessPiece):
    name = "B"
    def_cost = 3
    vects = ((1, 1), (1, -1), (-1, 1), (-1, -1))
    
    def get_move_cells(self):
        return get_all_scales(self.pos, self.vects)


class Rook(ChessPiece):
    name = "R"
    def_cost = 4
    vects = ((1, 0), (-1, 0), (0, 1), (0, -1))

    def get_move_cells(self):
        return get_all_scales(self.pos, self.vects)


class Queen(ChessPiece):
    name = "Q"
    def_cost = 8
    vects = Bishop.vects + Rook.vects

    def get_move_cells(self):
        return get_all_scales(self.pos, self.vects)


class King(ChessPiece):
    name = "K"    
    def_cost = 1000000

    def get_move_cells(self):
        x, y = self.pos
        new_positions = []
        
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                new_positions.append((x + dx, y + dy))

        return [[i] for i in new_positions if is_valid_cell(i)]


def position_evaluate(board):
    return board.sum_cost


@profile
def filter_pieces(board, pos, piece_class, color, allowed_classes):
    
    assert piece_class in allowed_classes

    get = board.const_get_func()

    for moves_list in piece_class(pos, color).move_cells():
        pieces = []
        for move in moves_list:
            if get(move) is not None:
                cp = get(move)

                # Pawn hack
                if piece_class is Bishop and isinstance(cp, Pawn) and cp.color == color:
                    dx = -1 if cp.color == "W" else 1
                    if move[0] - pos[0] == dx:
                        pieces.append(cp)

                if isinstance(cp, allowed_classes):
                    pieces.append(cp)
                else:
                    break
        yield pieces


def filter_pieces2(board, pos, vec, allowed_classes):
    dx, dy = vec
    x, y = pos
    get = board.const_get_func()

    for scale in range(1, 8):
        nx = x + dx * scale
        ny = y + dy * scale

        if get((nx, ny)) is not None:
            p = get((nx, ny))
            if scale == 1:
                if isinstance(p, Pawn) and dy != 0:
                    if p.color == "W" and dx == 1:
                        yield p
                    elif p.color == "B" and dx == -1:
                        yield p
                    else:
                        return
                if isinstance(p, King):
                    yield p
                    return
            if isinstance(p, allowed_classes):
                yield p
            else:
                return



def all_pieces_can_hit(board, cell):
    for pieces_list in filter_pieces(board, cell, Knight, "W", (Knight,)):
        for p in pieces_list:
            yield [p]

    for vec in Bishop.vects:
        l = list(filter_pieces2(board, cell, vec, (Queen, Bishop)))
        if l != []:
            yield l

    for vec in Rook.vects:
        l = list(filter_pieces2(board, cell, vec, (Queen, Rook)))
        if l != []:
            yield l


def hit_order(board, cell, start_color):
    lists = list(all_pieces_can_hit(board, cell))
    cost = 0
    ccolor = start_color
    cfigure = board.get(cell)
    cost_coef = 1
    while True:
        lists.sort(key=lambda x: x[0].def_cost)
        for l in lists:
            if l[0].color == ccolor:
                cost += cost_coef * getattr(cfigure, "def_cost", 0)
                cfigure = l[0]
                yield l[0], cost
                del l[0]
                break
        else:
            break
        # remove empty lists
        lists = filter(None, lists)
        ccolor = rev_color[ccolor]
        cost_coef = -cost_coef


@profile
def hit_chain(board, pos):
    w_chain = []
    b_chain = []

    def add_to_chain(p, to_new):
        c = w_chain if p.color == "W" else b_chain
        if to_new:
            c.append([p])
        else:
            c[-1].append(p)

    x, y = pos

    for pieces_list in filter_pieces(board, pos, Knight, "W", (Knight,)):
        for p in pieces_list:
            add_to_chain(p, True)

    # contains hask for Pawn
    for pieces_list in filter_pieces(board, pos, Bishop, "W", (Bishop, Queen)):
        w_chain.append([])
        b_chain.append([])
        for p in pieces_list:
            add_to_chain(p, False)

    for pieces_list in filter_pieces(board, pos, Rook, "W", (Rook, Queen)):
        w_chain.append([])
        b_chain.append([])
        for p in pieces_list:
            add_to_chain(p, False)

    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue
            p = board.get((x + dx, y + dy))
            if isinstance(p, King):
                add_to_chain(p, True)

    res_w = []
    res_b = []
    for hc, res_c in ((b_chain, res_b), (w_chain, res_w)):
        hc = [i for i in hc if i != []]
        while hc != []:
            hc.sort(key = lambda x: x[0].def_cost)
            res_c.append(hc[0][0])
            del hc[0][0]
            hc = [i for i in hc if i != []]

    return res_w, res_b


def get_next_step(board, for_color, level=2):
    moves = None
    best_evaluate = None
    
    cfunc = lambda val: val if for_color == "W" else -val

    for piece in board:
        if piece.color == for_color:
            for mv in board.get_all_moves(piece):
                ppos = piece.pos
                board.move(piece, mv)

                if level != 1:
                    next_moves, new_val = get_next_step(board, rev_color[for_color], level - 1)
                    new_val = -new_val
                else:
                    new_val = cfunc(position_evaluate(board))
                    next_moves = []

                board.move(piece, ppos)

                if new_val > best_evaluate or best_evaluate is None :
                    best_evaluate = new_val
                    moves = [(piece.pos, mv)] + next_moves

            for hit in board.get_all_hits(piece):
                
                ppos = piece.pos
                removed_piece = board.get(hit)

                board.remove(hit)
                board.move(piece, hit)

                if level != 1:
                    next_moves, new_val = get_next_step(board, rev_color[for_color], level - 1)
                    new_val = -new_val
                else:
                    new_val = cfunc(position_evaluate(board))
                    next_moves = []
                
                board.move(piece, ppos)
                board.add(removed_piece)

                if best_evaluate is None or new_val > best_evaluate:
                    best_evaluate = new_val
                    moves = [(piece.pos, hit)] + next_moves

    return moves, best_evaluate


def knorre_vs_neumann():
    p = [Pawn(i, "B") for i in "A6,B7,C6,C7,G4,H5".split(",")]
    p += [Pawn(i, "W") for i in "A2,B2,C2,E4,H4,G2".split(",")]
    p += [Rook("D1", "W"), Rook("F5", "W"), Rook("G8", "B"), Rook("E8", "B")]
    p += [Knight("G5", "W"), Bishop("G3", "W"), Knight("E5", "B"), Bishop("D6", "B")]    
    return p + [King("B8", "B"), King("H1", "W"), Queen("C3", "W"), Queen("E7", "B")]    

def get_start_board():
    pieces = [Pawn("{}2".format(i), "W") for i in board_letters]
    pieces += [Pawn("{}7".format(i), "B") for i in board_letters]
    pieces += [Bishop("C1", "W"), Bishop("F1", "W")]
    pieces += [Bishop("C8", "B"), Bishop("F8", "B")]
    pieces += [Knight("B1", "W"), Knight("G1", "W")]
    pieces += [Knight("B8", "B"), Knight("G8", "B")]
    pieces += [Rook("A1", "W"), Rook("H1", "W")]
    pieces += [Rook("A8", "B"), Rook("H8", "B")]
    pieces += [Rook("A8", "B"), Rook("H8", "B")]
    pieces += [Queen("E8", "B"), Queen("E1", "W")]
    pieces += [King("D8", "B"), King("D1", "W")]
    return pieces

class Board(object):

    # board is list of pieces
    def __init__(self, pieces):
        self.pieces = pieces
        self.pieces_map = {piece.pos:piece for piece in self}
        self.sum_cost = sum(piece.cost for piece in pieces)

    def __iter__(self):
        return iter(self.pieces)

    def get_all_moves(self, piece):
        for linked_moves in piece.move_cells():
            for pos in linked_moves:
                if pos in self.pieces_map:
                    break
                yield pos

    def get_all_hits(self, piece):
        for linked_hits in piece.hit_cells():
            for pos in linked_hits:
                hited_piece = self.pieces_map.get(pos)
                if hited_piece is None:
                    continue
                elif hited_piece.color != piece.color:
                    yield pos
                break

    def get(self, pos):
        return self.pieces_map.get(pos)

    def const_get_func(self):
        return self.pieces_map.get

    def remove(self, pos):
        piece = self.pieces_map[pos]
        del self.pieces_map[pos]
        self.pieces.remove(piece)
        self.sum_cost -= piece.cost

    def add(self, piece):
        self.sum_cost += piece.cost
        self.pieces.append(piece)
        self.pieces_map[piece.pos] = piece

    def move(self, piece, pos):
        del self.pieces_map[piece.pos]
        piece.move(pos)
        self.pieces_map[pos] = piece


import contextlib
@contextlib.contextmanager
def time_it():    
    t = time.time()
    yield
    print time.time() - t

if __name__ == "__main__":
    board = Board(knorre_vs_neumann())

    # t = time.time()
    # moves, val = get_next_step(board, "W", 3)
    # print time.time() - t

    # print "best val =", val
    # for frm, to in moves:
    #     print to_str_pos(frm), to_str_pos(to)

    with time_it():
        for i in range(2000):
            hit_chain(board, to_tuple_pos("E5"))

    #with time_it():
    #    for i in range(2000):
    #        for f,c in hit_order(board, to_tuple_pos("E5"), "W"):
    #            pass
