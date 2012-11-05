from gcd import gcd

def tostr(x):
    return "{0[1]}/{0[2]}".format(x)

def add(x, y):
    xtp, xnum, xdenom = x
    ytp, ynum, ydenom = y
    ndenom = xdenom * ydenom
    nnum = xnum * ydenom + xdenom * ynum
    if xtp == 'basic':
        return 'basic', nnum, ndenom
    elif xtp == 'auto_simpl':
        cur_gcd = gcd(nnum, ndenom)
        return ('auto_simpl', 
                 nnum / cur_gcd, 
                 ndenom / cur_gcd)
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

    r5 = ('auto_simpl', 1, 3)
    r6 = add(r5, r5)
    print "{} + {} = {}".format(tostr(r5), tostr(r5), tostr(r6))

if __name__ == "__main__":
    exit(main())




