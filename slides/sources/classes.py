class Base:
    def __init__(self, x):
        self.x = x

    def func1(self):
        print(f'Base::func1(x={self.x})')


class Child(Base):
    def __init__(self, x, y):
        Base.__init__(self, x)
        self.y = y

    def func1(self):
        print(f'Child::func1(x={self.x}, y={self.y})')
        super().func1()


b = Base(1)


b2 = Base.__new__(Base, 1)
b2.__init__(1)
Base.__init__(b2, 1)


c = Child(11, 12)

b.func1()
print("--------------------")

c.func1()
print("--------------------")

f = b.func1
f()
print("--------------------")

f2 = Base.func1
f2(b)
print("--------------------")
