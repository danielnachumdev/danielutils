# tlist
-- _like `list` but with runtime type safety_

## Purpose - What am I solving?
The `tlist` class is designed to provide runtime type safety for lists while also being applicable for static typing analasis. It ensures that the elements stored in the list are of a specific type specified during initialization.


## Features
* Allows runtime type checking for list elements.
* Supports instantiation with a specific type using `tlist[type]`.
* Implements all the basic list operations like `append`, `extend`, `__setitem__`, `__add__`, `__mul__`, etc.
* Provides custom string representation using `__str__` and `__repr__` methods.
* Implements comparison operations like `__eq__`.
* Supports iteration over the elements of the list.
* Provides a convenient way to create a new `tlist` by extending an existing `tlist` or a regular list.
* Supports multiplying a `tlist` by an integer to create a new `tlist` with repeated elements.

In summary, `tlist` enhances the functionality of the built-in list class by adding runtime type safety, ensuring that the list only contains elements of a specific type.

## Usage
Behind the scenes, runtime type validation is happening on all of the modifying functions
```python
# Create a tlist of integers
my_list = tlist[int]()

# Append elements to the list
my_list.append(10)
my_list.append(20)
my_list.append(30)

# Extend the list from another tlist or list
other_list = tlist[int]([40, 50, 60])
my_list.extend(other_list)

# Perform list operations
print(my_list)  # Output: tlist [10, 20, 30, 40, 50, 60]
print(my_list[2])  # Output: 30
my_list[1] = 25
print(my_list)  # Output: tlist [10, 25, 30, 40, 50, 60]

# Multiply the list to create a new tlist with repeated elements
new_list = my_list * 3
print(new_list)  # Output: tlist [10, 25, 30, 40, 50, 60, 10, 25, 30, 40, 50, 60, 10, 25, 30, 40, 50, 60]

# Compare tlists
print(new_list == my_list)  # Output: False
print(new_list == my_list * 3)  # Output: True
```
