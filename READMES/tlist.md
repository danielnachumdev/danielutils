# tlist
-- _Like ```list``` but with runtime type safety_

Browse the code [here](../danielutils/Classes/TypedBuiltins/tlist.py)

## Key Features

* The class is defined using generics (```list[T]```) and the ```Generic``` class from the typing module. This allows you to specify a type parameter ```T``` when using the ```tlist``` class, indicating the expected type of the elements in the list.

* The ```tlist``` class overrides several methods and implements additional methods to enforce type safety. For example, the ```append``` method checks if the value being appended is of the correct type, and the ```extend``` method ensures that the elements being added to the list are of the correct type.

* The ```tlist``` class provides a constructor (```__init__```) that takes a type parameter (item) and initializes the list. It also stores the type parameter in the _params attribute.

* The ```tlist``` class overrides string representation methods (```__str__``` and ```__repr__```) to include the class name when converting the list to a string.

* The class provides overloaded versions of the `_additional_init` method to handle different initialization scenarios, such as initializing from an empty list or initializing from a set or dictionary.

* The class overloads operators such as `__eq__` (equality), `__add__` (addition), and `__mul__` (multiplication) to provide expected behavior for these operations when working with tlist objects.
