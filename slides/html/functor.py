import abc
import operator
from typing import Callable, Any


class IFunctor(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __add__(self, other) -> 'IFunctor':
        pass

    @abc.abstractmethod
    def __radd__(self, other) -> 'IFunctor':
        pass

    @abc.abstractmethod
    def dwrt(self, var) -> 'IFunctor':
        pass

    @abc.abstractmethod
    def __call__(self, **vars):
        pass

    @abc.abstractmethod
    def __str__(self) -> str:
        pass


class FunctorBase(IFunctor):
    def __add__(self, other) -> IFunctor:
        return Add(self, other)

    def __radd__(self, other) -> IFunctor:
        return Add(other, self)


class BinaryFunctorBase(FunctorBase):
    var1: IFunctor
    var2: IFunctor
    op: str
    calc: Callable[[Any, Any], Any]

    def __init__(self, var1, var2) -> None:
        self.var1 = var1 if isinstance(var1, IFunctor) else Constant(var1)
        self.var2 = var2 if isinstance(var2, IFunctor) else Constant(var2)

    def __str__(self) -> str:
        return f"{self.var1} {self.op} {self.var2}"

    def __call__(self, **vars):
        return self.calc(self.var1(**vars), self.var2(**vars))


class Add(BinaryFunctorBase):
    op = '+'
    calc = operator.add

    def __str__(self) -> str:
        return f"{self.var1} {self.op} {self.var2}"

    def __call__(self, **vars):
        return self.calc(self.var1(**vars), self.var2(**vars))

    def dwrt(self, var) -> IFunctor:
        return self.var1.dwrt(var) + self.var2.dwrt(var)


class Variable(FunctorBase):
    def __init__(self, name: str) -> None:
        self.name = name

    def dwrt(self, var) -> IFunctor:
        return 1 if self.name == var.name else 0

    def __call__(self, **vars):
        return vars[self.name]

    def __str__(self) -> str:
        return self.name


class Constant(FunctorBase):
    def __init__(self, val) -> None:
        self.val = val

    def dwrt(self, var) -> IFunctor:
        return self.__class__(0)

    def __call__(self, **vars):
        return self.val

    def __str__(self) -> str:
        return f"{self.val}"


def f(x):
    return x + x + x + 1

v1 = Variable('v1')

t = f(v1)

print(f"t = {t}")
print(f"t(v1=1) = {t(v1=1)}")
print(f"t(v1=5) = {t(v1=5)}")
