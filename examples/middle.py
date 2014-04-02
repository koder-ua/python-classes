def get_middle(x, y, z):
    max_v = x if x > y else y
    max_v = max_v if max_v > z else z

    min_v = x if x < y else y
    min_v = min_v if min_v < z else z

    return x + y + z - min_v - max_v
