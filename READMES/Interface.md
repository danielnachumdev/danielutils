# Interface
DISCLAIMER: 

you __should not__ use this in production code I havent covered all of the edge cases. Instead use the [builtin implementation](#built-in-implemetation-abcmeta)

TL;DR :

To jump to the showcase click [here](#usage-and-capabilities)

to jump to the implementation click [here](../danielutils/metaclasses/Interface.py)
## Preface
The target of this was to learn about python's metaclasses

## Introduction
Have you ever wanted to use object-oriented programming concepts in Python? Do you like interfaces? Well, you have come to the right place! In this post, I will explain how I created my own implementation of a Python metaclass that lets classes achieve a behavior of interfaces from OOP languages like Java. I believe that many Python developers use the OOP concepts that Python offers to create classes in their programs, but only a smaller subset of those know that you can achieve some different behaviors using some more advanced Python, and specifically today's star: metaclasses.

### What are metaclasses and why are they important?
Before I dive into my implementation, I'd like to provide a brief overview of what metaclasses are and why they are important in Python's object-oriented programming paradigm.
In Python, a metaclass is a class whose instances are classes. In other words, it is a class that defines the behavior of other classes. When you create a new class, Python uses its metaclass to create the class object.

Metaclasses are important because they allow you to customize the behavior of classes. With metaclasses, you can define how a class should be created, what attributes it should have, and how its methods should behave. This means you can create classes that are tailored to your specific needs.

One common use of metaclasses is to implement frameworks and libraries that require certain behavior from the classes they work with. For example, Django, a popular web framework, uses metaclasses to create database models that interact with a database. The metaclass ensures that each model has the necessary attributes and methods to work with the database.

Metaclasses can also be used to enforce design patterns, implement custom syntax, and provide advanced features such as automatic memoization or caching.
### Built In implemetation: ABCMeta
see [```from abc import ABC, ABCMeta```](https://docs.python.org/3/library/abc.html)

## Things i learned while developing this
* how to use and create metaclasses
* how to use the MRO
* more python reflection
* how to use and configure pylint
* how to use and configure github workflows
* I have improved even further my "decorator skills"

## Usage and capabilities
Things that came up in the implementation:
* I have explicitly handled edge cases relating to the MRO regarding deep inheritance. As in: which `__init__` function should `super().__init__(...)` call.
* I had to take care of multiple inheritance
* I have added implicit abstract method definition in addition to the explicit one like in ABCMeta
* I have implemented the interfaces in a way that they can have an `__init__` function for the inheritance's sake, but you still can't instantiate them. (This actually allows to create an Abstract Base Class in addition to the Interface)
* I have implemented generic handler for abstract functions
* I have implemented detection if a derived class implements all of the necessary functions or not and it will raise an error message specifying which functions are missing
* Note that in the usage example below I have intentionally didn't give any arguments to Shape and Quadrilateral although the `__init__` function expects one, to showcase that if a class is an interface it's `__init__` function is irrelevant in __direct invocation__. but if it is called through a `super().__init__(...)` call than it is indeed called as expected. (in this case it is not an interface but rather an abstract class)

<br/>
Given the following classic example code:

```python
from math import pi
from danielutils import Interface

# although here it's actually an abstract class
class Shape(metaclass=Interface):
    def __init__(self, name):
        self.name = name

    # explicit invocation
    @Interface.abstractmethod
    def area(self):
        pass
    
    # implicit invocation
    def circumference(self):
        ...

    def angles(self):
        ...

    def __str__(self):
        return f"{self.name}: {self.area()=} {self.circumference()=} {self.angles()=}"


class Circle(Shape):
    def __init__(self, r):
        super().__init__("Circle")
        self.r = r

    def area(self):
        return pi*self.r**2

    def circumference(self):
        return 2*pi*self.r

    def angles(self):
        return -1


class Quadrilateral(Shape):
    def angles(self):
        return 360


class Rectangle(Quadrilateral):
    def __init__(self, a, b, name: str = "Rectangle"):
        super().__init__(name)
        self.a = a
        self.b = b

    def area(self):
        return self.a*self.b

    def circumference(self):
        return 2*(self.a+self.b)


class Square(Rectangle):
    def __init__(self, size):
        super().__init__(size, size, "Square")

```
And now for the actual usage:
```python
>>> Shape()
    Exception has occurred: NotImplementedError
        'Shape' is an interface, Can't create instances

>>> Quadrilateral()
    Exception has occurred: NotImplementedError
        Can't instantiate 'Quadrilateral' because it is an interface. It is missing implementations for {'circumference', '__init__', 'area'}

>>> Circle(3)
    Circle: self.area()=28.274333882308138 self.circumference()=18.84955592153876 self.angles()=-1

>>> Rectangle(2, 4)
    Rectangle: self.area()=8 self.circumference()=12 self.angles()=360

>>> Square(4)
    Square: self.area()=16 self.circumference()=16 self.angles()=360
```

## Conclusion
I hope this has provided you with a better understanding of my what this mini project has taught me. Although it is definitely not what i would recommend to start with I really enjoyed this process.