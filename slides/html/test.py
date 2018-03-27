class Struct:
	@classmethod
	def unpack(cls, buffer):
		for name, vl in cls.__dict__.items():
			if isinstance(vl, Field):
				vl.size


class Field:
	sizes = {int: 4, bool: 1}
	def __init__(self, tp, size=None):
		self.tp = tp
		self.size = size if size is not None else self.sizes[tp]
	


class D(Struct):
	f_1 = Field(int, 6)
	f_2 = Field(int)
	f_3 = Field(str)
	c_4 = Field(str)


D(deco)
def func(): ...


D.unpack("fe4tq33")
# d.f1 = 2
# d.pack() -> "sf345234535"



