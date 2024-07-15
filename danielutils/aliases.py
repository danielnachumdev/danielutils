# import inspect
# from abc import ABC, abstractmethod
# from typing import cast, Generic, ParamSpec, TypeVar, Callable
# from .functions import isoftype
# from .reflection.Function import get_caller_name, get_function_return_type
# P = ParamSpec("P")
# A = TypeVar("A")
# B = TypeVar("B")


# class SubscribableBase(ABC):
#     """An abstract class that need __instanceCheck__ to be implemented
#         will create default functions such that isinstance will work with the new type
#         while it is used as all of the python's generic types
#     """
#     __slots__ = ("params",)

#     def __init__(self, *params):
#         if get_caller_name() != "__class_getitem__":
#             raise ValueError(
#                 f"{self.__class__.__name__} is a type-hint class, Cant instantiate.")
#         self.params = params[0] if type(params) in {list, tuple} else params

#     @classmethod
#     def __class_getitem__(cls, *params) -> type:
#         res: type = cast(type, cls(*params))
#         return res

#     @abstractmethod
#     def __instancecheck__(self, value) -> bool: ...


# class Supplier(SubscribableBase):
#     """create a type for functions to be a supplier function
#     """

#     def __instancecheck__(self, func) -> bool:
#         if not callable(func):
#             return False
#         signature = inspect.signature(func)
#         if len(signature.parameters) != 0:
#             return False

#         return_type = get_function_return_type(func)
#         if return_type is not None:
#             try:
#                 return isoftype(return_type(), self.params)
#             except:
#                 return False
#         return self.params is None


# class Consumer(SubscribableBase):
#     """create a type for functions to be a consumer function
#     """

#     def __instancecheck__(self, func) -> bool:
#         if not callable(func):
#             return False
#         if get_function_return_type(func) is not type(None):
#             return False
#         signature = inspect.signature(func)
#         if len(signature.parameters) != 1:
#             return False
#         param_type = next(iter(signature.parameters.values())).annotation
#         try:
#             return isoftype(param_type(), self.params)
#         except:
#             return False


# class BinaryConsumer(SubscribableBase, Generic[A, B]):
#     """create a type for functions to be a binary consumer function
#     """

#     def __instancecheck__(self, func) -> bool:
#         if self.params[-1] is not None:
#             return False
#         self.params = self.params[0]
#         if not callable(func):
#             return False
#         if get_function_return_type(func) is not type(None):
#             return False
#         signature = inspect.signature(func)
#         if len(signature.parameters) != 2:
#             return False
#         param_iter = iter(signature.parameters.values())
#         param_types = (next(param_iter).annotation(),
#                        next(param_iter).annotation())
#         try:
#             for value, value_type in zip(param_types, self.params):
#                 if not isoftype(value, value_type):
#                     return False
#             return True
#         except:
#             return False

# # class Comparer(SubscribableBase):
# #     def __instancecheck__(self, func) -> bool:
# #         if not callable(func):
# #             return False
# #         if get_function_return_type(func) not in {int, float, Union[int, float]}:
# #             return False
# #         signature = inspect.signature(func)
# #         if len(signature.parameters) != 2:
# #             return False
# #         param_iter = iter(signature.parameters.values())
# #         param1_type = next(param_iter).annotation
# #         param2_type = next(param_iter).annotation
# #         try:
# #             return param1_type == param2_type == self.params[0] == self.params[1]
# #         except:
# #             return False
# # class Predicate(SubscribableBase):
# #     """create a type for functions to be a consumer function
# #     """

# #     def __instancecheck__(self, func) -> bool:
# #         if not callable(func):
# #             return False
# #         signature = inspect.signature(func)
# #         if len(signature.parameters) != 0:
# #             return False

# #         return_type = get_function_return_type(func)
# #         try:
# #             return isoftype(return_type(), self.params)
# #         except:
# #             return False


# # ListTupleType: TypeAlias = Union[list, tuple]
# __all__ = [
#     "SubscribableBase",
#     "Supplier",
#     "Consumer",
#     "BinaryConsumer",
#     # "Predicate"
#     # "ListTupleType"
# ]
from typing import Callable, TypeVar, Union

Number = Union[int, float, complex]

A = TypeVar("A")
B = TypeVar("B")
U = TypeVar("U")
T = TypeVar("T")
# P = ParamSpec("P")

Supplier = Callable[[], T]
Runnable = Supplier[None]
Consumer = Callable[[T], None]
UnaryFunction = Callable[[U], T]
UnaryOperator = Callable[[T], T]
Predicate = Callable[[T], bool]

BinaryFunction = Callable[[A, B], T]
BinaryOperator = Callable[[T, T], T]
Comparator = Callable[[A, B], int]
BinaryConsumer = Callable[[T, T], None]

__all__ = [
    "UnaryFunction",
    "BinaryFunction",
    "UnaryOperator",
    "BinaryOperator",
    "Supplier",
    "Predicate",
    "Comparator",
    "Consumer",
    "BinaryConsumer",
    "Runnable",
]
