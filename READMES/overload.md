# `overload`
-- _Managing function overloads with specific resolutions_

Browse code [here](../danielutils//decorators//overload.py)
## Purpose - What am I solving?
The purpose of the `overload` class is to provide a solution for managing function overloads with specific resolutions. It allows developers to define multiple alternative functions for a given function and select the appropriate one based on the number and types of arguments passed.

## Features
* Creation of an `overload` object to manage function overloads.
* Ability to add alternative functions to the list of available options.
* Automatic selection of the appropriate function based on the number and types of arguments.
* Clear error messages when no suitable overload is found.

The class is designed to handle function overloads in a specific manner and does not infer the best guess for types. It only matches a specific resolution based on the number of arguments and their types, as defined in the function annotations.

## Usage
Here are some examples of how to use the overload class:

```python
from danielutils import overload

@overload
def greet(name: str):
    print(f"Hello, {name}!")

@greet.overload
def greet(age: int):
    print(f"You are {age} years old.")

@greet.overload
def greet(name: str, is_student: bool):
    if is_student:
        print(f"Hello, {name}! You are a student.")
    else:
        print(f"Hello, {name}! You are not a student.")

@greet.overload
def greet(name: str, age: int):
    print(f"Hello, {name}! You are {age} years old.")

@greet.overload
def greet(is_student: bool):
    if is_student:
        print("Hello, student!")
    else:
        print("Hello, non-student!")

# Call the greet function with different arguments
>>> greet("Alice")
    Hello, Alice!
>>> greet(25) 
    You are 25 years old.
>>> greet("Bob", 30) 
    Hello, Bob! You are 30 years old.
>>> greet(True)  
    Hello, student!
>>> greet("Eve", False) 
    Hello, Eve! You are not a student.
```