# `isoftype`
-- Check if an object is of a given type or any of its subtypes.

Browse code [here](../danielutils/Functions.py)

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