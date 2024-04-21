import unittest

import math
from typing import Union, List as t_list
from danielutils.metaclasses.interface import Interface  # type:ignore
from danielutils.reflection import get_python_version  # type:ignore

if get_python_version() >= (3, 9):
    from builtins import list as t_list
Number = Union[int, float]


class TestInterface(unittest.TestCase):
    def test_no_implementation(self):
        class Interface1(metaclass=Interface):
            def foo(self):
                ...

        class MyClass(Interface1):
            pass

        with self.assertRaises(NotImplementedError):
            instance = MyClass()

    def test_multiple_inheritance_and_multiple_implementation(self):
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

    def test_inheritance_with_dummy_class(self):
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

    def test_inheritance_with_more_interfaces(self):
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

    def test_classic_use_case(self):
        class Shape(metaclass=Interface):
            def get_name(self) -> str:  # type:ignore
                pass

            def get_area(self) -> float:  # type:ignore
                pass

            def get_circumfarence(self) -> float:  # type:ignore
                pass

            def __str__(self) -> str:
                return f"{self.get_name()}: area-{self.get_area()}, circumfarence-{self.get_circumfarence()}"

        class Rectangel(Shape):
            def __init__(self, a: Number, b: Number):
                self.a, self.b = a, b

            def get_name(self) -> str:
                return "Rectangle"

            def get_area(self):
                return self.a * self.b

            def get_circumfarence(self) -> float:
                return (self.a + self.b) * 2

        class Square(Rectangel):
            def __init__(self, size: Number):
                super().__init__(size, size)

            def get_name(self) -> str:
                return "Square"

        class Circle(Shape):
            def __init__(self, radius: Number):
                self.radius = radius

            def get_name(self) -> str:
                return "Circle"

            def get_area(self):
                return math_.pi * self.radius ** 2

            def get_circumfarence(self) -> float:
                return 2 * math_.pi * self.radius

        class ColoredObject(metaclass=Interface):
            def get_color(self) -> str:  # type:ignore
                pass

        class ColoredCircle(Circle, ColoredObject):
            def __init__(self, radius: Number, color):
                super().__init__(radius)
                self.color = color

            def get_color(self):
                return self.color

            def __str__(self) -> str:
                return super().__str__() + f" color-{self.color}"

        shapes: t_list[Shape] = [
            Circle(2),
            Square(2),
            Rectangel(2, 3),
            ColoredCircle(5, "red")
        ]
        self.assertTrue(isinstance(shapes[3], Circle))
        self.assertTrue(isinstance(shapes[3], ColoredCircle))
        self.assertTrue(isinstance(shapes[3], Shape))

    def test_advanced_case(self):
        class Interface1(metaclass=Interface):
            def __init__(self) -> None:
                self.x = 5

            def foo(self):
                ...

            def foofoo(self) -> None:
                print("foofoo")

        class Interface2(metaclass=Interface):
            def bar(self):
                """_summary_
                """
                ...

        class MyClass(Interface1, Interface2):
            def __init__(self) -> None:
                super().__init__()

            def foo(self) -> None:
                print("foo")

            def bar(self) -> None:
                print(self.x)
                print("bar")

        with self.assertRaises(NotImplementedError):
            Interface1()

        with self.assertRaises(NotImplementedError):
            Interface2()

        # This should create an instance of MyClass successfully
        instance = MyClass()
        instance.foo()
        instance.foofoo()
        instance.bar()

    def test_inheritance_with_dummy_class_and_init(self):
        class Shape(metaclass=Interface):
            def __init__(self, name: str):
                self.name = name

            def __str__(self) -> str:
                return f"{self.name}: {self.area()=}, {self.circumfarence()=}, {self.sum_inner_angle()=}"

            def area(self) -> float:  # type:ignore
                ...

            def circumfarence(self) -> float:  # type:ignore
                ...

            def sum_inner_angle(self) -> float:  # type:ignore
                ...

        class Circle(Shape):
            def __init__(self, r: float):
                super().__init__("Circle")
                self.r = r

            def area(self) -> float:
                return self.r ** 2 * math_.pi

            def circumfarence(self) -> float:
                return 2 * math_.pi * self.r

            def sum_inner_angle(self) -> float:
                return math_.inf

        class Quadrilateral(Shape):
            def __init__(self, name: str):
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
                return self.size ** 2

            def circumfarence(self) -> float:
                return 4 * self.size

        class Square2(Quadrilateral2):
            def __init__(self, size: float):
                super().__init__("Square")
                self.size = size

            def area(self) -> float:
                return self.size ** 2

            def circumfarence(self) -> float:
                return 4 * self.size

        with self.assertRaises(NotImplementedError):
            Shape()  # type:ignore

        with self.assertRaises(NotImplementedError):
            Quadrilateral()  # type:ignore

        Circle(4)
        Square(4)
        Square2(4)

    def test_deeper_inheritance(self):
        class Shape(metaclass=Interface):

            def __init__(self, name: str):
                self.name = name

            def area(self) -> float:  # type:ignore
                ...

            def circumference(self) -> float:  # type:ignore
                ...

            def angles(self) -> int:  # type:ignore
                ...

            def __str__(self):
                return f"{self.name}: {self.area()=}, {self.circumference()=}, {self.angles()=}"

        class Circle(Shape):

            def __init__(self, radius: Number):
                super().__init__("Circle")

                self.radius = radius

            def area(self):
                return math_.pi * (self.radius ** 2)

            def circumference(self):
                return 2 * math_.pi * self.radius

            def angles(self):
                return -1

        class Quadrilateral(Shape):

            def __init__(self, name: str):
                super().__init__(name)

            def angles(self):
                return 360

        class Rectangle(Quadrilateral):

            def __init__(self, a: Number, b):
                super().__init__("Rectangle")

                self.a = a
                self.b = b

            def area(self):
                return self.a * self.b

            def circumference(self):
                return 2 * self.a + 2 * self.b

        class Square(Rectangle):

            def __init__(self, size: Number):
                super().__init__(a=size, b=size)

                self.name = "Square"

        Rectangle(10, 20)
        Square(10)
        Circle(6.4)

    def test_completely_empty(self):
        class Interface1(metaclass=Interface):
            pass

        class MyClass(Interface1):
            pass

        with self.assertRaises(NotImplementedError):
            Interface1()
        MyClass()
