from private_test import A as PA

class B(PA):
    def __init__(self):
        self.__x = 1

class A(PA):
    def __init__(self):
        self.__x = 1


print(B().__dict__)
print(A().__dict__)
print(PA().__dict__)
