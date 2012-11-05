#/usr/bin/env python

from gcd import gcd

class BasicRational(object):
    """basic rational number"""

    def __init__(self, numerator, denominator):
        self.numerator = numerator
        self.denominator = denominator

    def __add__(self, y):
        nd = self.denominator * y.denominator
        nn = self.numerator * y.denominator + \
                y.numerator * self.denominator
        return self.__class__(nn, nd)

    def __neg__(self):
        return self.__class__(-self.numerator, self.denominator)

    def __sub__(self, y):
        return self + (-y)

    def __str__(self):
        return "{}/{}".format(self.numerator, self.denominator)

    def __repr__(self):
        return str(self)


class AutoSimplifiedRN(BasicRational):
    """Auto simplified rational number"""

    def __init__(self, numerator, denominator):
        current_gcd = gcd(numerator, denominator)
        self.numerator = numerator / current_gcd
        self.denominator = denominator / current_gcd


b1 = AutoSimplifiedRN(1, 2)
b2 = AutoSimplifiedRN(1, 3)
b3 = b2 - b1 - b1
print b1, b2, b3
