#!/usr/bin/env python

source_code = "1 + 2 + (3 - 4)"
code = ('+', 
			('+', 1, 2), 
			('-', 3, 4))

def evaluate(val):
	if isinstance(val, int):
		res = val
	else:
		operator, oper1, oper2 = val
		assert operator in "+-", "Unknown operator " + operator

		v1 = evaluate(oper1)
		v2 = evaluate(oper2)

		if operator == '+':
			res = v1 + v2
		elif operator == '-':
			res = v1 - v2

	return res

print "evaluate({}) = {}".format(source_code, evaluate(code))


#-------------------------------------------------------------------------------

source_code = "2 * 2 + (3 - 4)"
code = ('+', 
			('*', 2, 2), 
			('-', 3, 4))

def evaluate_2(val):
	
