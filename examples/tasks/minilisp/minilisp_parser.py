#!/usr/bin/env python

def skip_spaces(program, pos=0):
    while program[pos].isspace():
        pos += 1
    return pos

def parse_str(program, pos):
    assert program[pos] == '"'
    next_pos = program.index('"', pos + 1)
    return program[pos + 1: next_pos], next_pos + 1

def parse_int(program, pos):
    if program[pos] == '-':
        pos += 1
        sign = -1
    else:
        sign = 1

    assert program[pos].isdigit()
    int_v = ""
    while program[pos].isdigit():
        int_v += program[pos]
        pos += 1

    return int(int_v), pos

def parse(program):
    return _parse(program.strip(), 0)[0]

def _parse(program, pos):
    assert program.startswith('(')
    assert program.endswith(')')

    pos = skip_spaces(program, pos + 1)

    oper = program[pos]
    pos += 1
    operands = []

    while True:
        pos = skip_spaces(program, pos)
        if program[pos] == ')':
            pos += 1
            break
        if program[pos] == '(':
            operand, pos = _parse(program, pos)
            operands.append(operand)
        elif program[pos] == '"':
            operand, pos = parse_str(program, pos)
            operands.append(operand)
        else:
            assert program[pos] == '-' or program[pos].isdigit()
            operand, pos = parse_int(program, pos)
            operands.append(operand)

    return (oper,) + tuple(operands), pos

