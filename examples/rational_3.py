def nod(x, y):
    x = abs(x)
    y = abs(y)
    return _nod(max(x, y), min(x, y))

def _nod(x, y):
    if y == 0:
        return x
    return nod(y, x % y)

class BasicRational(object):
    "basic rational number"

    def __init__(self, num, denom):
        self.num = num
        self.denom = denom

    def __add__(self, y):
        nd = self.denom * y.denom
        nn = self.num * y.denom + y.num * self.denom
        return self.__class__(nn, nd)

    def __neg__(self):
        return self.__class__(-self.num, self.denom)

    def __sub__(self, y):
        return self + (-y)

    def __str__(self):
        return "{}/{}".format(self.num, self.denom)

    def __repr__(self):
        return str(self)

class AutoSimpl(BasicRational):
    "Auto simplified rational number"
    def __init__(self, num, denom):
        cur_nod = nod(num, denom)
        self.num = num / cur_nod
        self.denom = denom / cur_nod


b1 = AutoSimpl(1, 2)
b2 = AutoSimpl(1, 3)
b3 = b2 - b1 - b1
print b1, b2, b3
