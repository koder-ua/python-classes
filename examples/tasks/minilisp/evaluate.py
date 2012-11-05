#!/usr/bin/env python
# -*- coding:utf8 -*-

from nodes import to_nodes

def evaluate_procedural(parsed_prog):
    if isinstance(parsed_prog, (int, str)):
        return parsed_prog

    assert isinstance(parsed_prog, tuple), "Program should be a tuple"
    assert len(parsed_prog) > 0, "Program should not be empty"

    oper = parsed_prog[0]
    operands = [evaluate_procedural(i) for i in parsed_prog[1:]]

    if oper == '+':
        assert len(operands) > 0
        res = operands[0]
        for val in operands[1:]:
            res += val
    elif oper == '-':
        assert len(operands) > 0
        res = operands[0]
        for val in operands[1:]:
            res -= val
    elif oper == 'print':
        print operands
    else:
        assert False, "Unknown operand " + oper
    return res

def evaluate_oop(parsed_prog):
    nodes = to_nodes(parsed_prog)
    return nodes.evaluate()