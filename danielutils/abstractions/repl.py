import copy, re
from typing import Any, Callable, Union, Tuple as t_tuple, List as t_list, Dict as t_dict
from ..reflection import get_python_version  # pylint :disable=relative-beyond-top-level

if get_python_version() >= (3, 9):
    from builtins import tuple as t_tuple, list as t_list, dict as t_dict  # type:ignore


class Argument:
    """a class to wrap an argument"""

    def __init__(self, name: str, optional: bool = False, flag: bool = False) -> None:
        self.name = name
        self.optional = optional
        self.flag = flag


class Command:
    """a class to wrap a command
    """

    def __init__(self, command: Union[Argument, str], callback: Callable,
                 explanation: str = "", *, options: t_tuple[Argument, ...] = tuple()) -> None:
        self.command = command if isinstance(
            command, Argument) else Argument(command)
        self.callback = callback
        self.explanation = explanation
        self.options = options

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        if len(args) > 0:
            if args[0] == "help":
                if self.explanation != "":
                    print(self.explanation)
                    return None
        return self.callback(*args, **kwargs)


class REPL:
    """a class to easily create a shell application and get functionality for free
    """

    # pylint: disable=dangerous-default-value
    def __init__(self, routes: t_list[Command], *, prompt_symbol: str = ">>> ", exit_keywords: set = {"exit", "quit"}):
        self.prompt_symbol = prompt_symbol
        self.exit_keywords = copy.copy(exit_keywords)
        self.routes: t_dict[str, Command] = {
            com.command.name: com for com in routes}

    def run(self) -> None:
        """runs the main loop for the shell

        Raises:
            e: any error if there is any
        """
        while True:
            prompt = input(self.prompt_symbol)
            if prompt in self.exit_keywords:
                break

            if prompt == "help":
                print("Available commands:")
                for com in list(self.routes.keys()) + list(self.exit_keywords):
                    print(f"\t{com}")
                continue

            prompt_parts = prompt.split()
            command = prompt_parts[0]
            if command in self.routes:
                try:
                    self.routes[command](*prompt_parts[1:])
                except TypeError as e:
                    msg = str(e)
                    if re.match(r".*missing.*required.*argument.*", msg):
                        print(f"'{command}' " + msg[msg.find("missing"):])
                    elif re.match(r".*takes.*arguments but.*given", msg):
                        print(f"'{command}' " + msg[msg.find("takes"):])
                    else:
                        raise e

            else:
                print(
                    "Invalid command. for help type 'help'.\nOr additionally you may try a command and then 'help'")


__all__ = [
    "REPL",
    "Command",
    "Argument"
]
