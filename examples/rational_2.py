def tostr(x):
    return "{0[1]}/{0[2]}".format(x)

def nod(x, y):
    x = abs(x)
    y = abs(y)
    return _nod(max(x, y), min(x, y))

def _nod(x, y):
    if y == 0:
        return x
    return nod(y, x % y)

def add(x, y):
    xtp, xnum, xdenom = x
    ytp, ynum, ydenom = y
    ndenom = xdenom * ydenom
    nnum = xnum * ydenom + xdenom * ynum
    if xtp == 'basic':
        return ('basic', nnum, ndenom)
    elif xtp == 'auto_simpl':
        cur_nod = nod(nnum, ndenom)
        return ('auto_simpl', 
                 nnum / cur_nod, 
                 ndenom / cur_nod)
    assert False, "Unsupported  rational type" + \
                  " for add" + xtp

def sub(x, y):
    ytp, ynum, ydenom = y
    return add(x, (ytp, -ynum, ydenom))

def main():
    r1 = ('basic', 1, 3)
    r2 = ('basic', 1, 2)
    print "tostr({!r}) = {}".format(r1, tostr(r1))

    r3 = sub(r2, r1)
    print "{} - {} = {}".format(tostr(r2), tostr(r1), tostr(r3))

    r4 = add(r1, r1)
    print "{} + {} = {}".format(tostr(r1), tostr(r1), tostr(r4))

    r5 = ('auto_simpl', r1[1], r1[2])
    r6 = add(r5, r5)
    print "{} + {} = {}".format(tostr(r5), tostr(r5), tostr(r6))

if __name__ == "__main__":
    exit(main())




