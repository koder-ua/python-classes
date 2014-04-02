import time
from abc import abstractmethod


from chess_base import board_letters, to_str_pos, to_tuple_pos, get_all_iscales, all_valid_ipositions
from chess_base import is_valid_icell, rev_color, color_index, color_sig, to_int_pos


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
        self.ipos = to_int_pos(pos)
        self.color = color
        self.cost = color_sig[self.color] * self.def_cost

    def copy(self):
        return self.__class__(self.ipos, self.color)

    @property
    def pos(self):
        return to_tuple_pos(self.ipos)

    @pos.setter
    def pos(self, value):
        self.ipos = to_int_pos(value)

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
        return (self.name, self.ipos)

    def full_name(self):
        return self.color + self.name

    def __str__(self):
        return "{}({!r}, {!r})".format(
                self.__class__.__name__, to_str_pos(self.pos), self.color)

    def __repr__(self):
        return str(self)

    def get_str_id(self):
        return "{}{}_{}".format(self.color, self.name, self.ipos)


get_x = lambda ip: ip // 16
get_y = lambda ip: ip & 0x0F


class Pawn(ChessPiece):
    name = "P"
    def_cost = 1

    move_vecs = {"W":(0x01, 1), "B":(-0x01, 6)}
    hit_vecs = {"W":(0x11, 0x1 - 0x10), "B":(-0x10 - 0x01, 0x10 - 0x01)}

    def __init__(self, pos, color):
        super(Pawn, self).__init__(pos, color)
        self.move_vec, self.double_move_cell = self.move_vecs[self.color]
        self.hv1, self.hv2 = self.hit_vecs[self.color]

    def move(self, pos):
        self.ipos = pos

    def eq_id(self):
        return (self.name, self.color, self.ipos)

    def get_move_cells(self):
        p1 = self.ipos + self.move_vec
        res = []
        if is_valid_icell(p1):
            res.append(p1)

        if get_y(self.ipos) == self.double_move_cell:
            p1 += self.move_vec 
            if is_valid_icell(p1):
                res.append(p1)
        return [res]

    def get_hit_cells(self):
        p1 = self.ipos + self.hv1
        res = []
        if is_valid_icell(p1):
            res.append([p1])

        p2 = self.ipos + self.hv2
        if is_valid_icell(p2):
            res.append([p2])

        #print self, to_str_pos(self.ipos), "=>", [to_str_pos(i[0]) for i in res]
        return res

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

    move_diffs = [-0x21, -0x1F, -0x12, -0x0E, 0x0E, 0x12, 0x1F, 0x21]

    def get_move_cells(self):
        ip = self.ipos
        ivp = is_valid_icell
        return [[ip + diff] for diff in self.move_diffs if ivp(ip + diff)]


class Bishop(ChessPiece):
    name = "B"
    def_cost = 3

    vects = [0x11, 0x0F, -0x0F, -0x11]
    
    def get_move_cells(self):
        return get_all_iscales(self.ipos, self.vects)


class Rook(ChessPiece):
    name = "R"
    def_cost = 4
    vects = [0x10, -0x10, 0x01, -0x01]

    def get_move_cells(self):
        return get_all_iscales(self.ipos, self.vects)


class Queen(ChessPiece):
    name = "Q"
    def_cost = 8
    vects = Bishop.vects + Rook.vects

    def get_move_cells(self):
        return get_all_iscales(self.ipos, self.vects)


class King(ChessPiece):
    name = "K"    
    def_cost = 1000000

    move_diffs = [-0x11, -0x10, -0x0F, -0x01, 0x01, 0x0F, 0x10, 0x11] 

    def get_move_cells(self):
        return [[self.ipos + diff] 
                    for diff in self.move_diffs 
                        if is_valid_icell(self.ipos + diff)]


def position_evaluate(board):
    return board.sum_cost


all_pieces_classes = (King, Queen, Rook, Bishop, Knight, Pawn)

text_to_piece = {}
for pc in all_pieces_classes:
    text_to_piece[pc.name] = pc


dxy_map = {
           -0x11:(-1, -1), 
           -0x10:(-1, 0),
           -0x0F:(-1, 1),
           -0x01:(0, -1),
           0x11:(1, 1), 
           0x10:(1, 0),
           0x0F:(1, -1),
           0x01:(0, 1),
           }


max_steps = {}

class PrepareMaxStepMap(object):
    for vec, (dx, dy) in dxy_map.items():
        for x in range(8):
            if dx == 1:
                max_x = 8 - x
            elif dx == -1:
                max_x = x + 1
            else:
                max_x = 8

            for y in range(8):
                if dy == 1:
                    max_y = 8 - y
                elif dy == -1:
                    max_y = y + 1
                else:
                    max_y = 8

                max_steps[(x * 0x10 + y, vec)] = min(max_x, max_y)
del PrepareMaxStepMap


def filter_pieces(board, pos, vec, allowed_classes):
    get = board.pieces_map.get
    dx, dy = dxy_map[vec]
    npos = pos

    for scale in range(1, max_steps[(pos, vec)]):

        npos += vec

        if get(npos) is not None:
            p = get(npos)
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


def build_hit_cache(cache, should_be_free_map):
    for piece_class in all_pieces_classes:
        for pos in all_valid_ipositions:
            for color in "BW":
                p = piece_class(pos, color)
                for hit_vec in p.hit_cells():
                    should_be_free = set()
                    for hit_pos in hit_vec:
                        cache.setdefault(hit_pos, set()).add(p.get_str_id())
                        should_be_free_map[(hit_pos, p.get_str_id())] = should_be_free.copy()
                        should_be_free.add(hit_pos)

@profile
def all_pieces_can_hit2(board, cell, cache={}, should_be_free_map={}):
    if cache == {}:
        print "build_hit_cache"
        build_hit_cache(cache, should_be_free_map)

    ps = {p.get_str_id() for p in board}
    get = board.const_get_func()
    possible_attackers = ps & cache[cell]

    attackers = []
    while True:
        add_at_least_one = False
        attackers_str = set()
        
        for possible_attacker in possible_attackers:
            if not (ps & should_be_free_map[(cell, possible_attacker)]):
                attackers.append([get(int(possible_attacker[3:]))])
                attackers_str.add(possible_attacker)
                add_at_least_one = True

        if not add_at_least_one:
            break

        #print list(attackers)
        ps -= attackers_str
        possible_attackers -= attackers_str

    return attackers


def all_pieces_can_hit(board, cell):
    get = board.const_get_func()
    for pos in Knight(cell, "W").hit_cells():
        p = get(pos[0])
        if isinstance(p, Knight):
            yield [p]

    for vec in Bishop.vects:
        l = list(filter_pieces(board, cell, vec, (Queen, Bishop)))
        if l:
            yield l

    for vec in Rook.vects:
        l = list(filter_pieces(board, cell, vec, (Queen, Rook)))
        if l:
            yield l


@profile
def hit_order(board, cell, start_color):
    b = board.copy()
    lists = list(all_pieces_can_hit2(b, cell))
    ccolor = start_color

    while True:
        lists.sort(key=lambda x: x[0].def_cost)
        for l in lists:
            if l[0].color == ccolor:
                fg = l[0].copy()
                b.remove(cell)
                b.move(l[0], cell)
                yield fg, position_evaluate(b)
                del l[0]
                break
        else:
            break
        # remove empty lists
        lists = filter(None, lists)
        ccolor = rev_color[ccolor]


def get_next_step(board, for_color, level=2):
    moves, new_value = _get_next_step(board, for_color, level, "")
    return moves, new_value - position_evaluate(board)


def is_better_move(curr, new, color):
    if new is None:
        return False
    return  curr is None or \
            (new > curr and color == "W") or \
            (new < curr and color == "B")


def _get_next_step(board, for_color, level=2, pstep="", hits_enabled=True):
    debug = False
    moves = []
    best_evaluate = None

    hit_checked = set()

    if 0 == level:
        if debug:
            print pstep + "empty"
        return [], position_evaluate(board)

    for piece in list(board):
        if piece.color == for_color:
            for mv in board.get_all_moves(piece):

                if debug:
                    print pstep + "mv ", piece, to_str_pos(mv)

                ppos = piece.ipos
                board.move(piece, mv)
                if level == 1:
                    next_moves = []
                    new_val = position_evaluate(board)
                else:
                    next_moves, new_val = _get_next_step(board, rev_color[for_color], level - 1, pstep + "    ")
                board.move(piece, ppos)

                if is_better_move(best_evaluate, new_val, for_color):
                    best_evaluate = new_val
                    moves = [(piece.ipos, mv)] + next_moves

            if hits_enabled:
                for hit in board.get_all_hits(piece):
                    if hit in hit_checked:
                        continue
                    else:
                        figures, evals = zip(*hit_order(board, hit, for_color))
                        best_after_this_color_move = (min if for_color == 'W' else max)(evals[::2])
                        
                        # need find best move after this position, disable hits to avoid internal loop
                        # apply hits
                        if evals[1::2]:
                            best_after_other_color_move = (max if for_color == 'W' else min)(evals[1::2])
                        else:
                            assert False

                        b = board.copy()
                        for figure in figures[:evals.index(best_after_other_color_move)]:
                            b.remove(hit)
                            print figure, to_str_pos(hit)
                            b.move(b.get(figure.ipos), hit)
                        _, new_eval = _get_next_step(b, for_color, 1, pstep + "    ", False)

                        if is_better_move(best_evaluate, new_eval, for_color):
                            best_evaluate = new_eval
                            moves = [(figures[0].ipos, hit)] + next_moves

                        if is_better_move(best_evaluate, best_after_this_color_move, for_color):
                            best_evaluate = best_after_this_color_move
                            moves = [(figures[0].ipos, hit)] + next_moves

    return moves, best_evaluate if best_evaluate is not None else position_evaluate(board)


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
        self.pieces_map = {piece.ipos:piece for piece in self}
        self.sum_cost = sum(piece.cost for piece in pieces)

    def copy(self):
        return self.__class__([i.copy() for i in self.pieces])

    def __iter__(self):
        return iter(self.pieces)

    def get_all_moves(self, piece):
        for linked_moves in piece.move_cells():
            for pos in linked_moves:
                if pos in self.pieces_map:
                    break
                yield pos

    def get_all_hits(self, piece):
        get = self.const_get_func()
        for linked_hits in piece.hit_cells():
            for pos in linked_hits:
                hited_piece = get(pos)
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
        self.pieces_map[piece.ipos] = piece

    def move(self, piece, pos):
        del self.pieces_map[piece.ipos]
        piece.ipos = pos
        self.pieces_map[pos] = piece

    @classmethod
    def parse(cls, *text_pieces):
        pieces = []
        for text_piece in text_pieces:
            tp, pos = text_piece.split(" ")
            color, ttp = tp
            pieces.append(text_to_piece[ttp](pos, color))
        return cls(pieces)


import contextlib
@contextlib.contextmanager
def time_it():    
    t = time.time()
    yield
    print time.time() - t

if __name__ == "__main__":
    board = Board(knorre_vs_neumann())

    t = time.time()
    for frm, to in get_next_step(board, "W", 2)[0]:
        print to_str_pos(fro), to_str_pos(to)
    print time.time() - t

    # print "best val =", val
    # for frm, to in moves:
    #     print to_str_pos(frm), to_str_pos(to)

    #for f,c in hit_order(board, to_int_pos("E5"), "W"):
    #    print f, c
