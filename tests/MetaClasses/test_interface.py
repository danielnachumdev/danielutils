import math
import pytest
from ...danielutils.MetaClasses.Interface import Interface


def test_no_implementation():
    class Interface1(metaclass=Interface):
        def foo(self):
            ...

    class MyClass(Interface1):
        pass

    with pytest.raises(NotImplementedError):
        instance = MyClass()


def test_multiple_inheritance_and_multiple_implemetation():
    class Interface1(metaclass=Interface):
        def foo(self):
            ...

    class Interface2(metaclass=Interface):
        def bar(self):
            ...

    class MyClass(Interface1, Interface2):
        def foo(self):
            pass

        def bar(self):
            pass

    # This should create an instance of MyClass successfully
    instance = MyClass()


def test_inheritance_with_dummy_class():
    class Interface1(metaclass=Interface):
        def foo(self):
            ...

    class AbstractClass(Interface1, metaclass=Interface):
        pass

    class MyClass(AbstractClass):
        def foo(self):
            pass

    # This should create an instance of MyClass successfully
    instance = MyClass()


def test_inheritance_with_more_interfaces():
    class Interface1(metaclass=Interface):
        def foo(self):
            ...

    class Interface2(Interface1, metaclass=Interface):
        def bar(self):
            ...

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

    shapes: list[Shape] = [
        Circle(2),
        Square(2),
        Rectangel(2, 3),
        ColoredCircle(5, "red")
    ]
    assert isinstance(shapes[3], Circle)
    assert isinstance(shapes[3], ColoredCircle)
    assert isinstance(shapes[3], Shape)


def test_advanced_case():
    class Interface1(metaclass=Interface):
        def __init__(self):
            self.x = 5

        def foo(self):
            ...

        def foofoo(self):
            print("foofoo")

    class Interface2(metaclass=Interface):
        def bar(self):
            """_summary_
            """
            ...

    class MyClass(Interface1, Interface2):
        def __init__(self):
            super().__init__()

        def foo(self):
            print("foo")

        def bar(self):
            print(self.x)
            print("bar")

    with pytest.raises(NotImplementedError):
        Interface1()

    with pytest.raises(NotImplementedError):
        Interface2()

    # This should create an instance of MyClass successfully
    instance = MyClass()
    instance.foo()
    instance.foofoo()
    instance.bar()


def test_inheticane_with_dummy_class_and_init():
    class Shape(metaclass=Interface):
        def __init__(self, name: str):
            self.name = name

        def __str__(self) -> str:
            return f"{self.name}: {self.area()=}, {self.circumfarence()=}, {self.sum_inner_angle()=}"

        def area(self) -> float:
            ...

        def circumfarence(self) -> float:
            ...

        def sum_inner_angle(self) -> float:
            ...

    class Circle(Shape):
        def __init__(self, r: float):
            super().__init__("Circle")
            self.r = r

        def area(self) -> float:
            return self.r**2*math.pi

        def circumfarence(self) -> float:
            return 2*math.pi*self.r

        def sum_inner_angle(self) -> float:
            return math.inf

    class Quadrilateral(Shape):
        def __init__(self, name):
            super().__init__(name)

        def sum_inner_angle(self) -> float:
            return 360

    class Quadrilateral2(Shape):
        def sum_inner_angle(self) -> float:
            return 360

    class Square(Quadrilateral):
        def __init__(self, size: float):
            super().__init__("Square")
            self.size = size

        def area(self) -> float:
            return self.size**2

        def circumfarence(self) -> float:
            return 4*self.size

    class Square2(Quadrilateral2):
        def __init__(self, size: float):
            super().__init__("Square")
            self.size = size

        def area(self) -> float:
            return self.size**2

        def circumfarence(self) -> float:
            return 4*self.size
    with pytest.raises(NotImplementedError):
        Shape()

    with pytest.raises(NotImplementedError):
        Quadrilateral()

    Circle(4)
    Square(4)
    Square2(4)


def test_deeper_inheritance():
    class Shape(metaclass=Interface):

        def __init__(self, name: str):
            self.name = name

        def area(self):
            ...

        def circumference(self):
            ...

        def angles(self):
            ...

        def __str__(self):
            return f"{self.name}: {self.area()=}, {self.circumference()=}, {self.angles()=}"

    class Circle(Shape):

        def __init__(self, radius):
            super().__init__("Circle")

            self.radius = radius

        def area(self):
            return math.pi * (self.radius ** 2)

        def circumference(self):
            return 2 * math.pi * self.radius

        def angles(self):
            return -1

    class Quadrilateral(Shape):

        def __init__(self, name):
            super().__init__(name)

        def angles(self):
            return 360

    class Rectangle(Quadrilateral):

        def __init__(self, a, b):
            super().__init__("Rectangle")

            self.a = a
            self.b = b

        def area(self):
            return self.a * self.b

        def circumference(self):
            return 2 * self.a + 2 * self.b

    class Square(Rectangle):

        def __init__(self, size):
            super().__init__(a=size, b=size)

            self.name = "Square"

    Rectangle(10, 20)
    Square(10)
    Circle(6.4)


def test_completly_empty():
    class Interface1(metaclass=Interface):
        pass

    class MyClass(Interface1):
        pass
    with pytest.raises(NotImplementedError):
        Interface1()
    MyClass()
