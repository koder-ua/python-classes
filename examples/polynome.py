from itertools import izip_longest

class Polynome(object):
	def __init__(self, *coefs):
		self.coefs = list(coefs)

		while self.coefs != [] and self.coefs[-1] == 0:
			del self.coefs[-1]

	def copy(self):
		return self.__class__(*self)

	def __getitem__(self, pos):
		if pos >= len(self):
			return 0
		return self.coefs[pos]

	def __setitem__(self, pos, val):
		dl = pos - len(self)
		if dl > 0:
			self.coefs += [0] * dl
		self.coefs[pos] = val

	def __delitem__(self, pos):
		if pos >= len(self):
			return
		self.coefs[pos] = 0

	def __iter__(self):
		return iter(self.coefs)

	def __len__(self):
		return len(self.coefs)

	def __add__(self, val):
		if isinstance(val, (int, float, long)):
			return self + Polynome(val)
		else:
			assert isinstance(val, Polynome)
			ncoefs = izip_longest(self, val, fillvalue=0)
			return self.__class__(*(a + b for a, b in ncoefs))

	def __radd__(self, val):
		return self + val

	def __mul__(self, val):
		if isinstance(val, (int, float, long)):
			coefs = (i * val for i in self)
		else:
			assert isinstance(val, Polynome)
			coefs = [0] * (len(self) + len(val) - 1)

			for pow1, coef1 in enumerate(self):
				for pow2, coef2 in enumerate(val):
					coefs[pow1 + pow2] += coef1 * coef2

		return self.__class__(*coefs)

	def __rmul__(self, val):
		return self * val

	def __div__(self, val):
		return self * (1.0 / val)

	def __sub__(self, val):
		return self + (-val)

	def __rsub__(self, val):
		return -self + val

	def __neg__(self):
		return self.__class__(*(-i for i in self))

	def __pow__(self, val):
		assert isinstance(val, (int, long))
		assert val > 0

		if 1 == val:
			res = self.copy()
		else:
			res = self
			for _ in range(val - 1):
				res = res * self

		return res

	def __call__(self, val):
		xs = [coef * (val ** i) for i,coef in enumerate(self)]
		return sum(xs)

	def __str__(self):
		res = []
		if len(self) > 0 and self[0] != 0:
			res.append(str(self[0]))

		if len(self) > 1 and self[1] != 0:
			res.append("{}x".format(self[1]))

		for i, val in enumerate(self.coefs[2:]):
			if val != 0:
				if 1 == val:
					res.append("x^{}".format(i + 2))
				else:
					res.append("{}x^{}".format(val, i + 2))

		return " + ".join(res[::-1])

	def __eq__(self, val):
		return list(self) == list(val)



x = Polynome(0, 1)
p = 2 * x ** 2 + 3 - 3 * x**4
print p == Polynome(3, 0, 2, 0, -3)
print p(2)

#print (x + 1) ** 135
