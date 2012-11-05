def gcd(x, y):
    x = abs(x)
    y = abs(y)
    return _gcd(max(x, y), min(x, y))

def _gcd(x, y):
    if y == 0:
        return x
    return gcd(y, x % y)

