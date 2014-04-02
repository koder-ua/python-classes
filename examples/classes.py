auto = ((x, y), (vec_x, vec_y), acceleration_level)

def set_accel_level1(auto, al):
    return (auto[0], auto[1], al)

def set_deccel_level1(auto, dl):
    return (auto[0], auto[1], -dl)

def set_wheel_pos1(auto, wp):
    pass

def tick(auto):
    (x, y), (vec_x, vec_y), al = auto            
    x += vec_x
    y += vec_y

    vec_x += 3 * al if al > 0 else 12 * al

    if al < 0:
        vec_y += 12 * al
    else:
        vec_y += 3 * al

    return (x, y), (vec_x, vec_y), al





class ZAZ(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vec_x = 0
        self.vec_y = 0
        self.al = 0

    def set_accel_level(self, al):
        self.al = al

    def tick(self):
        self.x += self.vec_x
        self.y += self.vec_y

        vec_x += 3 * al if al > 0 else 12 * al

        if al < 0:
            vec_y += 12 * al
        else:
            vec_y += 3 * al

        return (x, y), (vec_x, vec_y), al


















