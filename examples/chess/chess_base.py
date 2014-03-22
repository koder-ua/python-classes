board_letters = "ABCDEFGH"


def to_str_pos(tuple_pos):
    return board_letters[tuple_pos[0]] + str(tuple_pos[1] + 1)


def to_tuple_pos(str_pos):
    if isinstance(str_pos, tuple):
        return str_pos
    char, pos = str_pos
    return (board_letters.index(char), int(pos) - 1)


all_valid_poses = {(x,y) for x in range(8) for y in range(8)}


is_valid_cell = all_valid_poses.__contains__


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


