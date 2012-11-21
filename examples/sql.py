class Expression(object):
	def __eq__(self, other):
		return EQ(self, other)

	def __lt__(self, other):
		return LT(self, other)

	def __gt__(self, other):
		return GT(self, other)

	def __and__(self, other):
		return AND(self, other)

	def __ne__(self, other):
		return NE(self, other)


class TwoOpExpr(Expression):
	def __init__(self, v1, v2):
		self.v1 = v1
		self.v2 = v2

	def __str__(self):
		return "({} {} {})".format(self.v1, self.op, self.v2)

	def __call__(self, **params):
		v1 = self.v1(**params) if isinstance(self.v1, Expression) else self.v1
		v2 = self.v2(**params) if isinstance(self.v2, Expression) else self.v2
		return self.func(v1, v2)


class Field(Expression):
	def __init__(self, name):
		self.name = name

	def __str__(self):
		return self.name

	def __call__(self, **params):
		return params[self.name]


class EQ(TwoOpExpr):
	op = '='
	def func(self, v1, v2):
		return v1 == v2


class GT(TwoOpExpr):
	op = '>'
	def func(self, v1, v2):
		return v1 > v2

class LT(TwoOpExpr):
	op = '<'
	def func(self, v1, v2):
		return v1 < v2

class AND(TwoOpExpr):
	op = 'AND'
	def func(self, v1, v2):
		return v1 and v2

class NE(TwoOpExpr):
	op = '<>'
	def func(self, v1, v2):
		return v1 != v2

x = Field('x')
y = Field('y')

print (( x < y ) & ((x < 17) & (y != 3)))(x=7, y=13)

