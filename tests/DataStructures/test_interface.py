from danielutils import Interface


class IA(metaclass=Interface):
    pass


class A1:
    def __init__(self, z):
        self.z = z


class A2:
    def __init__(self, x):
        self.x = x


class B(A1, A2):
    def __init__(self, x, y):
        A1.__init__(self, x+y)
        A2.__init__(self, x)
        self.y = y

    def __str__(self):
        return f"{self.x}, {self.y}"


print(B(1, 2))
