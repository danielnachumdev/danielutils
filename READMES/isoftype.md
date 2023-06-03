# `isoftype`
-- _Check if an object is of a given type or any of its subtypes._

Browse code [here](../danielutils/Functions/isoftype.py)

## Purpose - What am I solving?
The purpose of the `isoftype` function is to determine whether an object is of a specific type or any of its subtypes. It provides a flexible type checking mechanism that accounts for various scenarios, including nested structures, unions, generics, and callable types. The function allows for both strict and non-strict type checking, providing different levels of accuracy based on the requirements.

## Features
* Check if an object is of a specific type or any of its subtypes.
* Handle nested structures, including lists, tuples, dictionaries, and sets.
* Support unions and optional types.
* Handle generators and iterables.
* Handle literal types.
* Check callable types, including lambda functions.
* Provide warning messages for ambiguous cases.
* Handle various type origin scenarios, such as generics, type variables, and forward references.

The `isoftype` function offers a comprehensive solution for type checking in Python, accommodating different scenarios and providing flexibility in determining the compatibility of objects with specific types or subtypes.

In conclusion, `isoftype` is a powerful type checking function that simplifies the process of verifying object types and their relationships, enabling developers to write more robust and flexible code.


## Usage
Here are some examples demonstrating the usage of the isoftype function:
* Examples that **can** be achieved with the builtin `isinstance`
    * Example 1: Basic Type Checking
        ```python
        # Check if an object is of type int
        result = isoftype(42, int)
        print(result)  # Output: True

        # Check if an object is of type str
        result = isoftype("Hello", str)
        print(result)  # Output: True

        # Check if an object is of type list
        result = isoftype([1, 2, 3], list)
        print(result)  # Output: True

        # Check if an object is of type float
        result = isoftype(3.14, float)
        print(result)  # Output: True

        # Check if an object is of type dict
        result = isoftype({"name": "John", "age": 30}, dict)
        print(result)  # Output: True
        ```
    * Example 2: Subtype Checking
        ```python
        class Shape:
            pass

        class Circle(Shape):
            pass

        class Rectangle(Shape):
            pass

        # Check if an object is of type Shape or any of its subtypes
        result = isoftype(Circle(), Shape)
        print(result)  # Output: True

        result = isoftype(Rectangle(), Shape)
        print(result)  # Output: True
        ```
* Examples that **can't** be achieved with the builtin `isinstance`
    * Example 3: Handling Union Types
        ```python
        from typing import Union

        # Check if an object is of type int or str
        result = isoftype(42, Union[int, str])
        print(result)  # Output: True

        result = isoftype("Hello", Union[int, str])
        print(result)  # Output: True

        # Check if an object is of type float or bool
        result = isoftype(3.14, Union[float, bool])
        print(result)  # Output: True

        result = isoftype(True, Union[float, bool])
        print(result)  # Output: True
        ```
    * Example 4: Handling Iterables
        ```python
        # Check if an object is an iterable of integers
        result = isoftype([1, 2, 3], Iterable[int])
        print(result)  # Output: True

        # Check if an object is an iterable of strings
        result = isoftype(("apple", "banana", "cherry"), Iterable[str])
        print(result)  # Output: True

        # Check if an object is a set of floats
        result = isoftype({3.14, 2.718, 1.618}, Set[float])
        print(result)  # Output: True
        ```
These examples demonstrate the versatility of the isoftype function in handling different type checking scenarios. You can use it to check basic types, subtypes, union types, and even **complex data structures**.