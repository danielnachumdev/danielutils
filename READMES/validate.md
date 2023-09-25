# `@validate`
-- _Protecting Your Code from Type-related Disasters._

Browse code [here](../danielutils/decorators//validate.py)
## Purpose - What am I solving?
The `validate` decorator is designed to validate the annotations and types of the arguments and return value of a function. It provides a convenient way to enforce type checking and ensure that the function is used correctly.

## Features
* Validates the annotations and types of the arguments and return value of a function.
* Allows `'None'` as a default value for any argument.
* Exempts commonly used keywords such as `'self'`, `'cls'`, `'args'`, and `'kwargs'` from validation.
* The decorator raises various exceptions if the validation fails:
    * `TypeError`: If the decorated object is not a callable function.
    * `EmptyAnnotationException`: If an argument is not annotated.
    * `InvalidDefaultValueException`: If an argument's default value is not of the annotated type.
    * `ValidationException`: If an argument's value is not of the expected type.
    * `InvalidReturnValueException`: If the return value is not of the expected type.

The decorator returns a wrapper function that performs the validation and calls the original function.

## Usage
To use the validate decorator, simply apply it to the desired function:

```python
@validate
def my_function(arg1: int, arg2: str) -> bool:
    return True
```
Alternatively, you can pass a boolean or a callable as an argument to control the strictness of the validation:

```python
@validate(strict=True)
def my_function(arg1: int, arg2: str) -> bool:
    return True
```
The decorator will enforce the specified type annotations and perform the necessary validation before calling the function.