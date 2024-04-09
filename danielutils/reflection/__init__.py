from .system_reflections import *  # this has to be first, the order matters!
from .file_reflection import *
from .function_reflections import *
from .get_traceback import *
from .module_reflections import *
from .class_reflection import *
from .callstack import *
from .interpreter import *
# def get_class(module_name: str, class_name: str) -> type:
#     """dynammically loads the module and returns the class from this file

#     Args:
#         module_name (str): name of python module, (typically a file name without extention)
#         class_name (str): the name of the wanted class

#     Returns:
#         type (type): The class
#     """
#     return dynamically_load(module_name, class_name)


# def get_function(module_name: str, func_name: str) -> Callable:
#     """dynammically loads the module and returns the function from this file

#     Args:
#         module_name (str): name of python module, (typically a file name without extention)
#         func_name (str): the name of the wanted function

#     Returns:
#         Callable: the function
#     """
#     return dynamically_load(module_name, func_name)


# def get_current_function() -> Callable:
#     """return the function that is calling this file

#     Returns:
#         Callable: function
#     """
#     return get_caller()


# def get_caller() -> Callable:
#     """returns the caller of the function thats using this function

#     Returns:
#         Callable: caller
#     """
#     name = get_caller_name(1)
#     module = get_caller_filename().removesuffix(".py")
#     return get_function(module, name)
