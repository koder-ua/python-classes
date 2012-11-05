#!/usr/bin/env python
# -*- coding:utf8 -*-

class Node(object):
    """Parsed three node"""

    def evaluate(self):
        raise NotImplemented("Node.evaluate is not implemented")

    def __str__(self):
        opers = ",\n".join(map(str, self.vals))
        return "{}(\n{}\n)".format(self.__class__.__name__,
                                   "    " +
                                    opers.replace("\n", "\n    "))


class Value(Node):
    """Node represent value"""
    def __init__(self, val):
        self.val = val

    def evaluate(self):
        return self.val

    def __str__(self):
        return "Val({!r})".format(self.val)

    def __repr__(self):
        return str(self)


class IntValue(Value):
    """Integer value node"""


class StrValue(Value):
    """String value node"""


class NonEmptyParametrizedNode(Node):
    def __init__(self, *kwargs):
        assert len(kwargs) > 0
        self.vals = kwargs


class Add(NonEmptyParametrizedNode):
    """Sum node"""

    def evaluate(self):
        # return reduce(lambda x,y : x + y, self.vals)
        res = self.vals[0].evaluate()
        for vl in self.vals[1:]:
            res += vl.evaluate()
        return res

class Sub(NonEmptyParametrizedNode):
    """Sum node"""

    def evaluate(self):
        # return reduce(lambda x,y : x + y, self.vals)
        res = self.vals[0].evaluate()
        for vl in self.vals[1:]:
            res -= vl.evaluate()
        return res

def _to_nodes(parsed_prog, nodes_map):
    assert isinstance(parsed_prog, tuple), "Program should be a tuple"
    assert len(parsed_prog) > 0, "Program should not be empty"

    parameters = []

    for node in parsed_prog[1:]:
        if isinstance(node, tuple):
            res = _to_nodes(node, nodes_map)
        elif isinstance(node, int):
            res = IntValue(node)
        elif isinstance(node, str):
            res = StrValue(node)
        else:
            assert False, "Unknown node type {!r}".format(node)
        parameters.append(res)

    return nodes_map[parsed_prog[0]](*parameters)

def to_nodes(parsed_prog):
    nmap = {
        '+' : Add,
        '-' : Sub
    }

    return _to_nodes(parsed_prog, nmap)

