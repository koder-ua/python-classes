#!/usr/bin/env python
# -*- coding:utf8 -*-
import sys
from minilisp_parser import parse
from evaluate import evaluate_procedural, evaluate_oop

def main(argv):
    code = '(+ 1 2 3 (+ 4 5 6))'
    pcode = parse(code)
    print evaluate_oop(pcode)

if __name__ == "__main__":
    exit(main(sys.argv))
