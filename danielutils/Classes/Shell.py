from typing import Any, Callable
import re


class Argument:
    def __init__(self, name: str, optional: bool = False, flag: bool = False) -> None:
        self.name = name
        self.optional = optional
        self.flag = flag


class Command:
    def __init__(self, command: Argument | str, callback: Callable, explanation: str = "", *, options: tuple[Argument, ...] = tuple()) -> None:
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
                    return
        return self.callback(*args, **kwargs)


class Shell:
    def __init__(self, routes: list[Command], *, prompt_symbol: str = ">>> ", exit_keywords: set = {"exit", "quit"}):
        self.prompt_symbol = prompt_symbol
        self.exit_keywords = exit_keywords
        self.routes: dict[str, Command] = {
            com.command.name: com for com in routes}

    def run(self) -> None:
        while True:
            prompt = input(self.prompt_symbol)
            if prompt in self.exit_keywords:
                break

            if prompt == "help":
                print("Available commands:")
                for com in list(self.routes.keys())+list(self.exit_keywords):
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
                        print(f"'{command}' "+msg[msg.find("missing"):])
                    elif re.match(r".*takes.*arguments but.*given", msg):
                        print(f"'{command}' "+msg[msg.find("takes"):])
                    else:
                        raise e

            else:
                print(
                    "Invalid command. for help type 'help'.\nOr additionally you may try a command and then 'help'")


__all__ = [
    "Shell",
    "Command",
    "Argument"
]
