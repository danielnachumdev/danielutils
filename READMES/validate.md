# validate
-- _Protecting Your Code from Type-related Disasters._

## Purpose
The `validate` decorator is designed to enforce type annotations and perform type validation for function arguments and return values. It ensures that the functions are used correctly with the expected types, validating the types of arguments, checking default values, enforcing annotation completeness, validating return types, and supporting strict type checking. By applying this decorator, you can improve code quality, reduce bugs related to incorrect types, and enhance code reliability by enforcing and validating type annotations automatically.

## Features
* Support for default values: The decorator handles default values for function arguments. It allows None as a default value for any argument and ensures that the default value matches the annotated type.

* Exclusion of common keywords: The decorator excludes commonly used keywords like 'self', 'cls', 'args', and 'kwargs' from validation. These keywords are typically used in specific contexts (e.g., instance methods, class methods, or function signatures with variable arguments) and are not subject to type validation.

* Handling of missing annotations: The decorator raises an EmptyAnnotationException if any argument is not annotated. It ensures that all arguments have explicit type annotations, promoting better code documentation and clarity.

* Support for strict type checking: The decorator allows for strict type checking by setting the strict parameter to True. In strict mode, the decorator enforces precise type matching, raising a ValidationException if an argument's value or the return value doesn't match the annotated type.

* Support for callable validation: The strict parameter of the decorator can also accept a Callable object. If a Callable is provided, it is treated as the function to be decorated, and strict is set to True implicitly.

* Compatibility with function signatures: The decorator works with functions of any signature, including functions with positional arguments, keyword arguments, and variable-length arguments.

* Preservation of function metadata: The decorator uses functools.wraps to preserve the original function's metadata, such as its name, module, and docstring. This ensures that the decorated function retains its identity and can be introspected correctly.

These features collectively enable the validate decorator to enhance code quality and reliability by enforcing type annotations and performing runtime type validation for function arguments and return values.