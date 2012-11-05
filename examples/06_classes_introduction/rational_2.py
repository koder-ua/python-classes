from gcd import gcd

def tostr(x):
    return "{0[num]}/{0[denom]}".format(x)

def mk_simpl(num, denom):
    return dict(num=num, denom=denom, add=add_simplified, sub=sub)

def mk_basic(num, denom):
    return dict(num=num, denom=denom, add=add_basic, sub=sub)

def add_basic(x, y):
    nd = x['denom'] * y['denom']
    nn = x['num'] * y['denom'] + x['denom'] * y['num']
    return mk_basic(nn, nd)

def add_simplified(x, y):
    res = add_basic(x, y)
    cur_gcd = gcd(res['num'], res['denom'])
    return mk_simpl(res['num'] / cur_gcd, res['denom'] / cur_gcd)

def add(x, y):
    return x['add'](x, y)

def sub(x, y):
    neg_x = y.copy()
    neg_x['num'] = -neg_x['num']
    return add(x, neg_x)

def main():
    r1 = mk_basic(1, 3)
    r2 = mk_basic(1, 2)

    print "tostr({!r}) = {}".format(r1, tostr(r1))

    r3 = sub(r2, r1)
    print "{} - {} = {}".format(tostr(r2), tostr(r1), tostr(r3))

    r4 = add(r1, r1)
    print "{} + {} = {}".format(tostr(r1), tostr(r1), tostr(r4))

    r5 = mk_simpl(1, 3)
    r6 = add(r5, r5)
    print "{} + {} = {}".format(tostr(r5), tostr(r5), tostr(r6))

if __name__ == "__main__":
    exit(main())

