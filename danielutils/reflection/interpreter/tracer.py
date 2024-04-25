import sys
from abc import ABC, abstractmethod
from enum import Enum
from types import FrameType
from typing import Any, Callable, Optional, Set as t_set, Dict as t_dict
from .python_version import get_python_version

if get_python_version() >= (3, 9):
    from builtins import set as t_set, dict as t_dict


# from danielutils import singleton
# @singleton
class Tracer(ABC):
    """
    A class to trace (during runtime) the flow of the currently executing code
    """
    _INSTANCE = None

    class EventType(Enum):
        """
        An enum class to represent all the types of possible events
        """
        CALL = "call"
        C_CALL = "c_call"
        RETURN = "return"
        C_RETURN = "c_return"

        @staticmethod
        def from_value(value: str):
            """
            Converts the given value to a Tracer.EventType instance
            """
            if value not in Tracer.EventType._value2member_map_:
                raise KeyError("Unknown value")
            return Tracer.EventType._value2member_map_[value]

    def __init__(
            self,
            *,
            skip_call: bool = False,
            skip_return: bool = False,
            skip_c_call: bool = True,
            skip_c_return: bool = True,
            functions: bool = True,
            classes: bool = True,
            instance_methods: bool = True,
            static_methods: bool = True,
            class_methods: bool = True,
            exclude: Optional[t_set[str]] = None
    ) -> None:

        self._call_dict: t_dict[Tracer.EventType, Callable] = {
            Tracer.EventType.CALL: self.on_call,
            Tracer.EventType.C_CALL: self.on_call_c,
            Tracer.EventType.RETURN: self.on_return,
            Tracer.EventType.C_RETURN: self.on_return_c,
        }
        self._skip_call = skip_call
        self._skip_return = skip_return
        self._skip_c_call = skip_c_call
        self._skip_c_return = skip_c_return
        self._functions = functions
        self._classes = classes
        self._instance_methods = instance_methods
        self._static_methods = static_methods
        self._class_methods = class_methods
        self._exclude = exclude if exclude is not None else set()
        from ...data_structures import Stack
        self._exclude_stack: Stack[str] = Stack()

    def _handler(self, stack_frame: FrameType, event_type: str, return_value: Optional[Any]):
        et = Tracer.EventType.from_value(event_type)
        if not self._should_skip(et, stack_frame):
            values = self.parse_event(stack_frame, et, return_value)
            self._call_dict[et](*values)
        return self._handler

    def _should_skip(self, et: 'Tracer.EventType', frame: FrameType) -> bool:
        func_name = frame.f_code.co_qualname

        if not self._exclude_stack.is_empty():
            if et in {Tracer.EventType.CALL, Tracer.EventType.C_CALL}:
                self._exclude_stack.push(func_name)
            else:
                self._exclude_stack.pop()
            return True
        if func_name in self._exclude:
            self._exclude_stack.push(func_name)
            return True

        if et == Tracer.EventType.CALL and self._skip_call or \
                et == Tracer.EventType.RETURN and self._skip_return or \
                et == Tracer.EventType.C_CALL and self._skip_c_call or \
                et == Tracer.EventType.C_RETURN and self._skip_c_return:
            return True

        # TODO add more cases
        return False

    def __enter__(self):
        if Tracer._INSTANCE is not None:
            raise RuntimeError("Can only have one active Tracer object at a time")
        Tracer._INSTANCE = self
        self.start_tracing()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        Tracer._INSTANCE = None
        self.stop_tracing()

    def start_tracing(self) -> None:
        sys.setprofile(self._handler)

    def stop_tracing(self) -> None:
        sys.setprofile(None)

    @abstractmethod
    def parse_event(self, frame: FrameType, et: EventType, return_value: Optional[Any]) -> tuple:
        pass

    @abstractmethod
    def on_call(self, *args, **kwargs) -> None:
        """
        A Handler for when a function is called
        """

    @abstractmethod
    def on_call_c(self, *args, **kwargs) -> None:
        """
        A Handler for when an underlying C function is called
        """

    @abstractmethod
    def on_return(self, *args, **kwargs) -> None:
        """
        A Handler for when a function returns
        """

    @abstractmethod
    def on_return_c(self, *args, **kwargs) -> None:
        """
        A Handler for when an underlying C function returns
        """


class ConsoleTracer(Tracer):
    # def __init__(self, *args, **kwargs) -> None:
    #     super().__init__(*args, **kwargs)

    def parse_event(self, frame: FrameType, event_type: Tracer.EventType, return_value: Optional[Any]) -> tuple:
        func_name: str = frame.f_code.co_qualname
        base: tuple = event_type, func_name
        final: tuple = base
        if return_value is not None:
            final = *base, return_value
        return final

    def on_call(self, *args, **kwargs) -> None:
        print(*args, **kwargs)

    def on_call_c(self, *args, **kwargs) -> None:
        print(*args, **kwargs)

    def on_return(self, *args, **kwargs) -> None:
        print(*args, **kwargs)

    def on_return_c(self, *args, **kwargs) -> None:
        print(*args, **kwargs)


__all__ = [
    "Tracer",
    "ConsoleTracer"
]
