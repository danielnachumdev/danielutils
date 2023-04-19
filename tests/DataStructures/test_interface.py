import math
from ...danielutils.DataStructures.Interface import Interface
import pytest


def test_no_implementation():
    class Interface1(metaclass=Interface):
        def foo(self):
            pass

    class MyClass(Interface1):
        pass

    with pytest.raises(NotImplementedError):
        instance = MyClass()


def test2():
    class Interface1(metaclass=Interface):
        def foo(self):
            pass

    class Interface2(metaclass=Interface):
        def bar(self):
            pass

    class MyClass(Interface1, Interface2):
        def foo(self):
            pass

        def bar(self):
            pass

    # This should create an instance of MyClass successfully
    instance = MyClass()


def test3():
    class Interface1(metaclass=Interface):
        def foo(self):
            pass

    class AbstractClass(Interface1, metaclass=Interface):
        pass

    class MyClass(AbstractClass):
        def foo(self):
            pass

    # This should create an instance of MyClass successfully
    instance = MyClass()


def test4():
    class Interface1(metaclass=Interface):
        def foo(self):
            pass

    class Interface2(Interface1, metaclass=Interface):
        def bar(self):
            pass

    class MyClass(Interface2):
        def foo(self):
            pass

        def bar(self):
            pass

    # This should create an instance of MyClass successfully
    instance = MyClass()


def test_classic_use_case():

    class Shape(metaclass=Interface):
        def get_name(self) -> str:
            pass

        def get_area(self) -> float:
            pass

        def get_circumfarence(self) -> float:
            pass

        def __str__(self) -> str:
            return f"{self.get_name()}: area-{self.get_area()}, circumfarence-{self.get_circumfarence()}"

    class Rectangel(Shape):
        def __init__(self, a, b):
            self.a, self.b = a, b

        def get_name(self) -> str:
            return "Rectangle"

        def get_area(self):
            return self.a*self.b

        def get_circumfarence(self) -> float:
            return (self.a+self.b)*2

    class Square(Rectangel):
        def __init__(self, size):
            super().__init__(size, size)

        def get_name(self) -> str:
            return "Square"

    class Circle(Shape):
        def __init__(self, radius):
            self.radius = radius

        def get_name(self) -> str:
            return "Circle"

        def get_area(self):
            return math.pi*self.radius**2

        def get_circumfarence(self) -> float:
            return 2*math.pi*self.radius

    class ColoredObject(metaclass=Interface):
        def get_color(self) -> str:
            pass

    class ColoredCircle(Circle, ColoredObject):
        def __init__(self, radius, color):
            super().__init__(radius)
            self.color = color

        def get_color(self):
            return self.color

        def __str__(self) -> str:
            return super().__str__()+f" color-{self.color}"

    shapes: list[Shape] = [Circle(2), Square(
        2), Rectangel(2, 3), ColoredCircle(5, "red")]
    for shape in shapes:
        print(shape)
        print(isinstance(shape, Shape))
        print(isinstance(shape, ColoredObject))
