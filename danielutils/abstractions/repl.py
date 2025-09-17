import copy, re
import logging
from typing import Any, Callable, Union, Tuple as Tuple, List as List, Dict as Dict
from ..reflection import get_python_version  # pylint :disable=relative-beyond-top-level
from ..logging_.utils import get_logger

if get_python_version() >= (3, 9):
    from builtins import tuple as Tuple, list as List, dict as Dict  # type:ignore
logger = get_logger(__name__)


class Argument:
    """a class to wrap an argument"""

    def __init__(self, name: str, optional: bool = False, flag: bool = False) -> None:
        logger.debug("Creating Argument: name=%s, optional=%s, flag=%s", name, optional, flag)
        self.name = name
        self.optional = optional
        self.flag = flag
        logger.debug("Argument created successfully: %s", name)


class Command:
    """a class to wrap a command
    """

    def __init__(self, command: Union[Argument, str], callback: Callable,
                 explanation: str = "", *, options: Tuple[Argument, ...] = tuple()) -> None:
        logger.debug("Creating Command: command=%s, explanation_length=%d, options_count=%d", command if isinstance(command, str) else command.name, len(explanation), len(options))
        self.command = command if isinstance(
            command, Argument) else Argument(command)
        self.callback = callback
        self.explanation = explanation
        self.options = options
        logger.debug("Command created successfully: %s", self.command.name)

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        logger.debug("Command '%s' called with args_count=%d, kwargs_count=%d", self.command.name, len(args), len(kwargs))
        if len(args) > 0:
            if args[0] == "help":
                logger.info("Help requested for command: %s", self.command.name)
                if self.explanation != "":
                    print(self.explanation)
                    logger.debug("Help explanation displayed for command: %s", self.command.name)
                    return None
        try:
            result = self.callback(*args, **kwargs)
            logger.debug("Command '%s' executed successfully", self.command.name)
            return result
        except Exception as e:
            logger.error("Command '%s' failed with %s: %s", self.command.name, type(e).__name__, e)
            raise


class REPL:
    """a class to easily create a shell application and get functionality for free
    """

    # pylint: disable=dangerous-default-value
    def __init__(self, routes: List[Command], *, prompt_symbol: str = ">>> ", exit_keywords: set = {"exit", "quit"}):
        logger.info("Initializing REPL with %d commands, prompt='%s', exit_keywords=%s", len(routes), prompt_symbol, exit_keywords)
        self.prompt_symbol = prompt_symbol
        self.exit_keywords = copy.copy(exit_keywords)
        self.routes: Dict[str, Command] = {
            com.command.name: com for com in routes}
        logger.debug("REPL initialized successfully with commands: %s", list(self.routes.keys()))

    def run(self) -> None:
        """runs the main loop for the shell

        Raises:
            e: any error if there is any
        """
        logger.info("Starting REPL main loop")
        while True:
            prompt = input(self.prompt_symbol)
            logger.debug("User input received: '%s'", prompt)
            
            if prompt in self.exit_keywords:
                logger.info("Exit keyword '%s' received, stopping REPL", prompt)
                break

            if prompt == "help":
                logger.info("Help command requested")
                print("Available commands:")
                for com in list(self.routes.keys()) + list(self.exit_keywords):
                    print(f"\t{com}")
                logger.debug("Help displayed with %d commands", len(self.routes) + len(self.exit_keywords))
                continue

            prompt_parts = prompt.split()
            command = prompt_parts[0]
            logger.debug("Processing command: '%s' with %d arguments", command, len(prompt_parts)-1)
            
            if command in self.routes:
                try:
                    logger.debug("Executing command: %s", command)
                    self.routes[command](*prompt_parts[1:])
                    logger.debug("Command '%s' completed successfully", command)
                except TypeError as e:
                    msg = str(e)
                    logger.warning("TypeError in command '%s': %s", command, msg)
                    if re.match(r".*missing.*required.*argument.*", msg):
                        print(f"'{command}' " + msg[msg.find("missing"):])
                    elif re.match(r".*takes.*arguments but.*given", msg):
                        print(f"'{command}' " + msg[msg.find("takes"):])
                    else:
                        logger.error("Unhandled TypeError in command '%s': %s", command, e)
                        raise e
                except Exception as e:
                    logger.error("Unexpected error in command '%s': %s: %s", command, type(e).__name__, e)
                    raise e
            else:
                logger.warning("Invalid command '%s' received", command)
                print(
                    "Invalid command. for help type 'help'.\nOr additionally you may try a command and then 'help'")
        
        logger.info("REPL main loop ended")


__all__ = [
    "REPL",
    "Command",
    "Argument"
]
