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
        logger.debug(f"Creating Argument: name={name}, optional={optional}, flag={flag}")
        self.name = name
        self.optional = optional
        self.flag = flag
        logger.debug(f"Argument created successfully: {name}")


class Command:
    """a class to wrap a command
    """

    def __init__(self, command: Union[Argument, str], callback: Callable,
                 explanation: str = "", *, options: Tuple[Argument, ...] = tuple()) -> None:
        logger.debug(f"Creating Command: command={command if isinstance(command, str) else command.name}, explanation_length={len(explanation)}, options_count={len(options)}")
        self.command = command if isinstance(
            command, Argument) else Argument(command)
        self.callback = callback
        self.explanation = explanation
        self.options = options
        logger.debug(f"Command created successfully: {self.command.name}")

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        logger.debug(f"Command '{self.command.name}' called with args_count={len(args)}, kwargs_count={len(kwargs)}")
        if len(args) > 0:
            if args[0] == "help":
                logger.info(f"Help requested for command: {self.command.name}")
                if self.explanation != "":
                    print(self.explanation)
                    logger.debug(f"Help explanation displayed for command: {self.command.name}")
                    return None
        try:
            result = self.callback(*args, **kwargs)
            logger.debug(f"Command '{self.command.name}' executed successfully")
            return result
        except Exception as e:
            logger.error(f"Command '{self.command.name}' failed with {type(e).__name__}: {e}")
            raise


class REPL:
    """a class to easily create a shell application and get functionality for free
    """

    # pylint: disable=dangerous-default-value
    def __init__(self, routes: List[Command], *, prompt_symbol: str = ">>> ", exit_keywords: set = {"exit", "quit"}):
        logger.info(f"Initializing REPL with {len(routes)} commands, prompt='{prompt_symbol}', exit_keywords={exit_keywords}")
        self.prompt_symbol = prompt_symbol
        self.exit_keywords = copy.copy(exit_keywords)
        self.routes: Dict[str, Command] = {
            com.command.name: com for com in routes}
        logger.debug(f"REPL initialized successfully with commands: {list(self.routes.keys())}")

    def run(self) -> None:
        """runs the main loop for the shell

        Raises:
            e: any error if there is any
        """
        logger.info("Starting REPL main loop")
        while True:
            prompt = input(self.prompt_symbol)
            logger.debug(f"User input received: '{prompt}'")
            
            if prompt in self.exit_keywords:
                logger.info(f"Exit keyword '{prompt}' received, stopping REPL")
                break

            if prompt == "help":
                logger.info("Help command requested")
                print("Available commands:")
                for com in list(self.routes.keys()) + list(self.exit_keywords):
                    print(f"\t{com}")
                logger.debug(f"Help displayed with {len(self.routes) + len(self.exit_keywords)} commands")
                continue

            prompt_parts = prompt.split()
            command = prompt_parts[0]
            logger.debug(f"Processing command: '{command}' with {len(prompt_parts)-1} arguments")
            
            if command in self.routes:
                try:
                    logger.debug(f"Executing command: {command}")
                    self.routes[command](*prompt_parts[1:])
                    logger.debug(f"Command '{command}' completed successfully")
                except TypeError as e:
                    msg = str(e)
                    logger.warning(f"TypeError in command '{command}': {msg}")
                    if re.match(r".*missing.*required.*argument.*", msg):
                        print(f"'{command}' " + msg[msg.find("missing"):])
                    elif re.match(r".*takes.*arguments but.*given", msg):
                        print(f"'{command}' " + msg[msg.find("takes"):])
                    else:
                        logger.error(f"Unhandled TypeError in command '{command}': {e}")
                        raise e
                except Exception as e:
                    logger.error(f"Unexpected error in command '{command}': {type(e).__name__}: {e}")
                    raise e
            else:
                logger.warning(f"Invalid command '{command}' received")
                print(
                    "Invalid command. for help type 'help'.\nOr additionally you may try a command and then 'help'")
        
        logger.info("REPL main loop ended")


__all__ = [
    "REPL",
    "Command",
    "Argument"
]
