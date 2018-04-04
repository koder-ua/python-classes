import types
import yaml


data = """
params:
    a: 1
    b: 2

O33:
    class: O1
    p1: 2
    p2: 3

O2:
    p1: 2
    p2: 3

instantiate: O33, O2
"""


class AllStatic(type):
    def __new__(mcls, name, base, dct):
        ndct = {}
        for name, v in dct.items():
            if isinstance(v, types.FunctionType):
                v = staticmethod(v)
            ndct[name] = v
        return super().__new__(mcls, name, bases, ndct)


class DI(metaclass=AllStatic):
    def param1(a: int, b: int) -> str:
        return f"{a}::{b}"

    def empty_objs(all_objs: List[IObject1]) -> List[IObject1]:
        return all_objs[:2]


class O1(IObject1):
    def __init__(self, p1: int, p2: int, param1: str):
        pass


class O2(IObject2):
    def __init__(self, p1: int, p2: int, empty_objs: List[IObject1]):
        pass


def create_system(instantiate: List[str],
                  config_params: Dict[str, Dict[str, Any]],
                  extra_params: Dict[str, Any],
                  lazy_params: Any,
                  classes: Dict[str, type]) -> Dict[str, Any]:
    pass
