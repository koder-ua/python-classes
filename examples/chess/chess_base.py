board_letters = "ABCDEFGH"


def to_int_pos(pos):
    if isinstance(pos, str):
        return to_int_pos(to_tuple_pos(pos))
    if isinstance(pos, int):
        return pos
    return pos[0] * 16 + pos[1]


def to_str_pos(tuple_pos):
    if isinstance(tuple_pos, int):
        return to_str_pos(to_tuple_pos(tuple_pos)) 
    return board_letters[tuple_pos[0]] + str(tuple_pos[1] + 1)


def to_tuple_pos(pos):
    if isinstance(pos, tuple):
        return pos

    if isinstance(pos, int):
        return (pos // 16, pos & 0x0F)

    char, pos = pos
    return (board_letters.index(char), int(pos) - 1)


all_valid_positions = {(x,y) for x in range(8) for y in range(8)}
all_valid_ipositions = set(map(to_int_pos, all_valid_positions))


is_valid_cell = all_valid_positions.__contains__
is_valid_icell = all_valid_ipositions.__contains__


rev_color = {"B":"W", "W":"B"}
color_index = {"W":0, "B":1}
color_sig = {"W":1, "B":-1}


def get_all_scales(pos, vects):
    x, y = pos
    res = []

    for dx, dy in vects:
        new_positions = []
        for scale in range(1, 8):
            npos = (x + dx * scale, y + dy * scale)
            if not is_valid_cell(npos):
                break
            new_positions.append(npos)
        res.append(new_positions)

    return res

def get_all_iscales(pos, vects):
    res = []
    for diff in vects:
        #print "diff =", diff, "pos =", to_str_pos(pos)
        new_positions = []
        npos = pos
        for scale in range(1, 8):
            npos += diff
            #print "npos =", to_str_pos(npos)
            if not is_valid_icell(npos):
                break
            new_positions.append(npos)
        res.append(new_positions)
    return res

