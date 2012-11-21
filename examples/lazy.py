#!/usr/bin/env python
# -*- coding:utf8 -*-

import functools

def lazy(func):
    @functools.wraps(func)
    def closure(*args, **kwargs):
        return Lazy(func, args, kwargs)
    return closure

class Lazy(object):
    def __init__(self, func, args, kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.result = None
        self.is_ready = False

    def __str__(self):
        return str(self.materialize())

    def materialize(self):
        if not self.is_ready:
            self.result = self.func(*self.args, **self.kwargs)
            self.is_ready = True
        return self.result

@lazy
def func(x, y):
    print "calculated"
    return x + y

res = func(1, 2)

print "before print"
print res


