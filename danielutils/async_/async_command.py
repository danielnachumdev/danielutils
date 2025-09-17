"""
Generic AsyncCommand class for standardized async command execution.

This module provides a comprehensive AsyncCommand class that encapsulates command execution
with state tracking, result handling, and CLI/GUI strategy support using async patterns.
"""

import asyncio
import logging
import os
import subprocess
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import List, Optional, Union, Callable, Dict, Literal
from datetime import datetime
from ..logging_.utils import get_logger

logger = get_logger(__name__)


@dataclass
class CommandResult:
    """Comprehensive result object for command execution."""
    args: List[str]
    returncode: int
    stdout: str
    stderr: str
    pid: int
    start_time: str
    end_time: str
    duration_seconds: float
    timeout_occurred: bool
    killed: bool
    success: bool
    command: str  # The original command string


@dataclass
class CommandResponse:
    success: bool
    output: str
    error: Optional[str] = None
    result: Optional[CommandResult] = None


class CommandState(Enum):
    """Enumeration of possible command states."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"
    KILLED = "killed"


class CommandType(Enum):
    """Enumeration of command types."""
    CLI = "cli"
    GUI = "gui"


@dataclass
class CommandExecutionResult:
    """Result of command execution with comprehensive details."""
    command: 'AsyncCommand'
    success: bool
    return_code: int
    stdout: str
    stderr: str
    execution_time: float
    state: CommandState
    killed: bool = False
    timeout_occurred: bool = False
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    pid: Optional[int] = None
    command_type: CommandType = CommandType.CLI
    exception: Optional[Exception] = None

    def __str__(self) -> str:
        """String representation of the result."""
        status = "SUCCESS" if self.success else "FAILED"
        if self.timeout_occurred:
            status = "TIMEOUT"
        elif self.killed:
            status = "KILLED"

        return f"CommandExecutionResult(command={self.command}, success={self.success}, return_code={self.return_code}, stdout='{self.stdout}', stderr='{self.stderr}', execution_time={self.execution_time}, state={self.state}, killed={self.killed}, timeout_occurred={self.timeout_occurred}, start_time={self.start_time}, end_time={self.end_time}, pid={self.pid}, command_type={self.command_type}, exception={self.exception}) - {status}"


class AsyncCommand:
    """
    Generic async command execution class with comprehensive state tracking and result handling.

    This class provides a unified interface for executing commands with support for:
    - Async execution with proper event loop management
    - State tracking (pending, running, completed, failed, timeout, killed)
    - Comprehensive result reporting (stdout, stderr, return code, execution time)
    - CLI/GUI execution strategies
    - Callback support for lifecycle events
    - Timeout handling
    - Process management (kill, wait)
    """
    logger: logging.Logger = logging.getLogger(__name__)

    def __init__(
            self,
            args: List[str],
            command_type: CommandType = CommandType.CLI,
            timeout: Optional[float] = None,
            cwd: Optional[Union[str, Path]] = None,
            env: Optional[Dict[str, str]] = None,
            on_start: Optional[Callable[['AsyncCommand'], None]] = None,
            on_complete: Optional[Callable[['AsyncCommand', CommandExecutionResult], None]] = None,
            on_error: Optional[Callable[['AsyncCommand', Exception], None]] = None,
    ):
        """
        Initialize the AsyncCommand.

        Args:
            args: Command arguments as a list of strings
            command_type: Type of command (CLI or GUI)
            timeout: Timeout in seconds (None for no timeout)
            cwd: Working directory for command execution
            env: Environment variables for command execution
            on_start: Callback called when command starts
            on_complete: Callback called when command completes
            on_error: Callback called when command fails
        """
        logger.debug("Initializing AsyncCommand with args=%s, command_type=%s, timeout=%s", args, command_type, timeout)
        self.args = args
        self.command_type = command_type
        if timeout is not None:
            if timeout <= 0.0:
                raise ValueError("timeout must be strictly positive")
        self.timeout = timeout
        self.cwd = Path(cwd) if cwd else None
        self.env = env or {}
        self.on_start = on_start
        self.on_complete = on_complete
        self.on_error = on_error

        # State management
        self._state = CommandState.PENDING
        self._process: Optional[subprocess.Popen] = None
        self._result: Optional[CommandExecutionResult] = None
        self._start_time: Optional[datetime] = None
        logger.debug("AsyncCommand initialized successfully with state=%s", self._state)

    @property
    def state(self) -> CommandState:
        """Get the current state of the command."""
        return self._state

    @property
    def is_running(self) -> bool:
        """Check if the command is currently running."""
        return self._state == CommandState.RUNNING

    @property
    def is_completed(self) -> bool:
        """Check if the command has completed (successfully or not)."""
        return self._state in [CommandState.COMPLETED, CommandState.FAILED, CommandState.TIMEOUT, CommandState.KILLED]

    @property
    def result(self) -> Optional[CommandExecutionResult]:
        """Get the execution result if available."""
        return self._result

    async def execute(self, timeout: Optional[float] = None) -> CommandExecutionResult:
        """
        Execute the command asynchronously.

        Args:
            timeout: Override the default timeout for this execution

        Returns:
            CommandExecutionResult: Comprehensive execution result

        Raises:
            RuntimeError: If command is not in pending state
        """
        # Log command execution start
        self.logger.info("Executing command (async)", extra={
            "data": {
                "command": " ".join(self.args),
                "command_args": self.args,
                "command_type": self.command_type.value,
                "timeout": timeout or self.timeout,
                "cwd": str(self.cwd) if self.cwd else None,
                "env_keys": list(self.env.keys()) if self.env else None
            }
        })

        # Check if command is in pending state
        if self._state != CommandState.PENDING:
            raise RuntimeError(f"Command is not in pending state: {self._state}")

        # Check if args is empty - this is considered an error
        if not self.args:
            end_time = datetime.now()
            result = CommandExecutionResult(
                command=self,
                success=False,
                return_code=-1,
                stdout="",
                stderr="Empty command arguments provided",
                execution_time=0.0,
                start_time=self._start_time,
                end_time=end_time,
                state=CommandState.FAILED
            )
            self._result = result
            self._state = CommandState.FAILED
            return result

        # Set initial state
        self._state = CommandState.RUNNING
        self._start_time = datetime.now()

        # Call on_start callback
        if self.on_start:
            self.on_start(self)

        try:
            # Execute based on command type
            if self.command_type == CommandType.CLI:
                result = await self._execute_cli_strategy(timeout)
            else:
                result = await self._execute_gui_strategy(timeout)

            return result

        except (OSError, ValueError, subprocess.SubprocessError, asyncio.TimeoutError) as e:
            # Handle unexpected errors
            end_time = datetime.now()
            execution_time = (end_time - self._start_time).total_seconds()

            result = CommandExecutionResult(
                command=self,
                success=False,
                return_code=-1,
                stdout="",
                stderr=f"Command execution failed: {str(e)}",
                execution_time=execution_time,
                state=CommandState.FAILED,
                start_time=self._start_time,
                end_time=end_time,
                command_type=self.command_type,
                exception=e
            )

            self._state = CommandState.FAILED
            self._result = result

            if self.on_error:
                self.on_error(self, e)

            return result

    async def _execute_cli_strategy(self, timeout: Optional[float] = None) -> CommandExecutionResult:
        """Execute using CLI strategy asynchronously."""
        start_time = self._start_time or datetime.now()
        effective_timeout = timeout if timeout is not None else self.timeout

        try:
            # Create subprocess
            # Merge environment variables with current environment
            env = os.environ.copy()
            if self.env:
                env.update(self.env)

            # Use asyncio.create_subprocess_exec instead of subprocess.Popen to avoid threading issues
            # Set encoding to UTF-8 for proper unicode support
            self._process = await asyncio.create_subprocess_exec(
                *self.args,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=str(self.cwd) if self.cwd else None,
                env=env
            )

            pid = self._process.pid
            self.logger.debug("CLI subprocess created (async)", extra={
                "data": {
                    "pid": pid,
                    "command": " ".join(self.args),
                    "timeout": effective_timeout
                }
            })

            # Wait for completion with timeout
            try:
                # Use asyncio.wait_for with the process directly instead of asyncio.to_thread
                stdout, stderr = await asyncio.wait_for(self._process.communicate(),
                                                        timeout=effective_timeout)
                returncode = self._process.returncode

                # Decode bytes to strings
                stdout = stdout.decode('utf8') if stdout else ""
                stderr = stderr.decode('utf8') if stderr else ""

                if returncode == 0:
                    self.logger.info("CLI subprocess completed successfully (async)", extra={
                        "data": {
                            "pid": pid,
                            "command": " ".join(self.args),
                            "returncode": returncode,
                            "stdout_length": len(stdout),
                            "stderr_length": len(stderr)
                        }
                    })
                else:
                    self.logger.warning("CLI subprocess completed with non-zero exit code (async)", extra={
                        "data": {
                            "pid": pid,
                            "command": " ".join(self.args),
                            "returncode": returncode,
                            "stderr_length": len(stderr)
                        }
                    })

            except asyncio.TimeoutError:
                # Kill the process on timeout
                self.logger.warning("CLI subprocess timed out, killing process (async)", extra={
                    "data": {
                        "pid": pid,
                        "command": " ".join(self.args),
                        "timeout": effective_timeout
                    }
                })

                try:
                    self._process.kill()
                    stdout, stderr = await self._process.communicate()
                    # Decode bytes to strings
                    stdout = stdout.decode('utf-8', errors='replace') if stdout else ""
                    stderr = stderr.decode('utf-8', errors='replace') if stderr else ""
                except (OSError, subprocess.SubprocessError, BaseException):
                    stdout, stderr = "", ""
                returncode = -1

                self.logger.error("CLI subprocess killed due to timeout (async)", extra={
                    "data": {
                        "pid": pid,
                        "command": " ".join(self.args),
                        "timeout": effective_timeout,
                        "stderr_length": len(stderr),
                        "stdout_length": len(stdout)
                    }
                })

                # Set timeout state and return early
                end_time = datetime.now()
                execution_time = (end_time - start_time).total_seconds()

                result = CommandExecutionResult(
                    command=self,
                    success=False,
                    return_code=returncode,
                    stdout=stdout or "",
                    stderr=stderr or "",
                    execution_time=execution_time,
                    state=CommandState.TIMEOUT,
                    timeout_occurred=True,
                    start_time=start_time,
                    end_time=end_time,
                    pid=pid,
                    command_type=self.command_type
                )

                self._state = CommandState.TIMEOUT
                self._result = result

                if self.on_complete:
                    self.on_complete(self, result)

                return result

        except (OSError, ValueError, subprocess.SubprocessError) as e:
            returncode = -1
            stdout = ""
            stderr = f"CLI command failed to start: {str(e)}"

            self.logger.error("CLI subprocess execution failed (async)", extra={
                "data": {
                    "command": " ".join(self.args),
                    "error": str(e),
                    "timeout": effective_timeout
                }
            })

        end_time = datetime.now()
        execution_time = (end_time - start_time).total_seconds()
        success = returncode == 0
        state = CommandState.COMPLETED if success else CommandState.FAILED

        # Check if this was a timeout
        timeout_occurred = False
        if returncode == -1 and effective_timeout is not None and execution_time >= effective_timeout * 0.9:
            state = CommandState.TIMEOUT
            timeout_occurred = True

        result = CommandExecutionResult(
            command=self,
            success=success,
            return_code=returncode,
            stdout=stdout or "",
            stderr=stderr or "",
            execution_time=execution_time,
            state=state,
            timeout_occurred=timeout_occurred,
            start_time=start_time,
            end_time=end_time,
            pid=self._process.pid if self._process else None,
            command_type=self.command_type
        )

        self._state = state
        self._result = result

        # Call appropriate callback based on result
        if not success and self.on_error:
            # Create a generic exception for non-zero return codes
            error = RuntimeError(f"Command failed with return code {returncode}")
            self.on_error(self, error)
        elif self.on_complete:
            self.on_complete(self, result)

        return result

    async def _execute_gui_strategy(self, timeout: Optional[float] = None) -> CommandExecutionResult:
        """Execute using GUI strategy asynchronously."""
        start_time = self._start_time or datetime.now()
        effective_timeout = timeout if timeout is not None else self.timeout

        try:
            # Create subprocess without capturing output
            # Merge environment variables with current environment
            env = os.environ.copy()
            if self.env:
                env.update(self.env)

            self._process = subprocess.Popen(
                self.args,
                shell=True,
                cwd=str(self.cwd) if self.cwd else None,
                env=env
            )

            pid = self._process.pid
            self.logger.debug("GUI subprocess created (async)", extra={
                "data": {
                    "pid": pid,
                    "command": " ".join(self.args),
                    "timeout": effective_timeout
                }
            })

            # Wait for completion with timeout
            try:
                returncode = await asyncio.wait_for(
                    asyncio.to_thread(self._process.wait),
                    timeout=effective_timeout
                )

                if returncode == 0:
                    self.logger.info("GUI subprocess completed successfully (async)", extra={
                        "data": {
                            "pid": pid,
                            "command": " ".join(self.args),
                            "returncode": returncode
                        }
                    })
                else:
                    self.logger.warning("GUI subprocess completed with non-zero exit code (async)", extra={
                        "data": {
                            "pid": pid,
                            "command": " ".join(self.args),
                            "returncode": returncode
                        }
                    })

            except asyncio.TimeoutError:
                # Kill the process on timeout
                self.logger.warning("GUI subprocess timed out, killing process (async)", extra={
                    "data": {
                        "pid": pid,
                        "command": " ".join(self.args),
                        "timeout": effective_timeout
                    }
                })

                try:
                    self._process.kill()
                    await asyncio.to_thread(self._process.wait)
                except (OSError, subprocess.SubprocessError, BaseException):
                    pass
                returncode = -1

                self.logger.error("GUI subprocess killed due to timeout (async)", extra={
                    "data": {
                        "pid": pid,
                        "command": " ".join(self.args),
                        "timeout": effective_timeout
                    }
                })

                # Set timeout state and return early
                end_time = datetime.now()
                execution_time = (end_time - start_time).total_seconds()

                result = CommandExecutionResult(
                    command=self,
                    success=False,
                    return_code=returncode,
                    stdout="",  # GUI commands don't capture output
                    stderr="",  # GUI commands don't capture output
                    execution_time=execution_time,
                    state=CommandState.TIMEOUT,
                    timeout_occurred=True,
                    start_time=start_time,
                    end_time=end_time,
                    pid=pid,
                    command_type=self.command_type
                )

                self._state = CommandState.TIMEOUT
                self._result = result

                if self.on_complete:
                    self.on_complete(self, result)

                return result

        except (OSError, ValueError, subprocess.SubprocessError) as e:
            returncode = -1
            self.logger.error("GUI subprocess execution failed (async)", extra={
                "data": {
                    "command": " ".join(self.args),
                    "error": str(e),
                    "timeout": effective_timeout
                }
            })

        end_time = datetime.now()
        execution_time = (end_time - start_time).total_seconds()
        success = returncode == 0
        state = CommandState.COMPLETED if success else CommandState.FAILED

        # Check if this was a timeout
        timeout_occurred = False
        if returncode == -1 and effective_timeout is not None and execution_time >= effective_timeout * 0.9:
            state = CommandState.TIMEOUT
            timeout_occurred = True

        result = CommandExecutionResult(
            command=self,
            success=success,
            return_code=returncode,
            stdout="",  # GUI commands don't capture output
            stderr="",  # GUI commands don't capture output
            execution_time=execution_time,
            state=state,
            timeout_occurred=timeout_occurred,
            start_time=start_time,
            end_time=end_time,
            pid=self._process.pid if self._process else None,
            command_type=self.command_type
        )

        self._state = state
        self._result = result

        # Call appropriate callback based on result
        if not success and self.on_error:
            # Create a generic exception for non-zero return codes
            error = RuntimeError(f"Command failed with return code {returncode}")
            self.on_error(self, error)
        elif self.on_complete:
            self.on_complete(self, result)

        return result

    def kill(self) -> bool:
        """
        Kill the running command.

        Returns:
            bool: True if the command was killed, False otherwise
        """
        self.logger.info("Attempting to kill command", extra={
            "data": {
                "command": " ".join(self.args),
                "state": self._state.value,
                "has_process": self._process is not None
            }
        })

        if not self._process or not self.is_running:
            self.logger.warning("Attempted to kill command that is not running", extra={
                "data": {
                    "command": " ".join(self.args),
                    "state": self._state.value,
                    "has_process": self._process is not None,
                    "is_running": self.is_running
                }
            })
            return False

        pid = self._process.pid
        try:
            self._process.kill()
            self._state = CommandState.KILLED

            self.logger.info("Command killed successfully", extra={
                "data": {
                    "command": " ".join(self.args),
                    "pid": pid,
                    "state": self._state.value
                }
            })
            return True
        except (OSError, subprocess.SubprocessError) as e:
            self.logger.error("Failed to kill command", extra={
                "data": {
                    "command": " ".join(self.args),
                    "pid": pid,
                    "error": str(e),
                    "error_type": type(e).__name__
                }
            })
            return False

    def cleanup(self) -> None:
        """Clean up resources and ensure proper shutdown."""
        if self._process:
            try:
                if self._process.poll() is None:
                    self._process.kill()
                self._process.wait(timeout=1.0)
            except (OSError, subprocess.SubprocessError, subprocess.TimeoutExpired):
                pass
            finally:
                self._process = None

    async def wait(self) -> CommandExecutionResult:
        """
        Wait for the command to complete.

        Returns:
            CommandExecutionResult: The execution result
        """
        self.logger.info("Waiting for command to complete", extra={
            "data": {
                "command": " ".join(self.args),
                "state": self._state.value
            }
        })

        if self._result:
            self.logger.debug("Command already completed, returning cached result", extra={
                "data": {
                    "command": " ".join(self.args),
                    "state": self._state.value,
                    "success": self._result.success
                }
            })
            return self._result

        # If not running, execute first
        if self._state == CommandState.PENDING:
            return await self.execute()

        # Wait for completion
        while not self.is_completed:
            await asyncio.sleep(0.1)

        self.logger.info("Command completed", extra={
            "data": {
                "command": " ".join(self.args),
                "state": self._state.value,
                "success": self._result.success if self._result else False
            }
        })

        return self._result

    def to_command_result(self) -> CommandResult:
        """Convert to CommandResult schema."""
        if not self._result:
            return CommandResult(
                success=False,
                return_code=-1,
                stdout="",
                stderr="Command not executed",
                execution_time=0.0
            )

        return CommandResult(
            success=self._result.success,
            return_code=self._result.return_code,
            stdout=self._result.stdout,
            stderr=self._result.stderr,
            execution_time=self._result.execution_time
        )

    def to_command_response(self) -> CommandResponse:
        """Convert to CommandResponse schema."""
        if not self._result:
            return CommandResponse(
                success=False,
                message="Command not executed",
                data={}
            )

        return CommandResponse(
            success=self._result.success,
            message="Command executed successfully" if self._result.success else "Command failed",
            data={
                "return_code": self._result.return_code,
                "stdout": self._result.stdout,
                "stderr": self._result.stderr,
                "execution_time": self._result.execution_time,
                "state": self._state.value,
                "pid": self._result.pid
            }
        )

    @staticmethod
    def _parse_command_string(command: str) -> List[str]:
        """
        Parse a command string into a list of arguments, handling quoted strings properly.

        This method intelligently splits command strings while preserving spaces within
        single or double quotes. It handles both single and double quotes correctly.

        Args:
            command: The command string to parse

        Returns:
            List[str]: List of parsed command arguments

        Examples:
            >>> _parse_command_string('echo "hello world"')
            ['echo', 'hello world']
            >>> _parse_command_string("git commit -m 'fix bug'")
            ['git', 'commit', '-m', 'fix bug']
            >>> _parse_command_string('cmd "arg with spaces" --flag value')
            ['cmd', 'arg with spaces', '--flag', 'value']
        """
        if not command.strip():
            return []

        args = []
        current_arg = ""
        in_quotes = False
        quote_char = None

        i = 0
        while i < len(command):
            char = command[i]

            if not in_quotes:
                if char in ['"', "'"]:
                    # Start of quoted string
                    in_quotes = True
                    quote_char = char
                elif char == ' ':
                    # Space outside quotes - end of current argument
                    if current_arg:
                        args.append(current_arg)
                        current_arg = ""
                else:
                    # Regular character
                    current_arg += char
            else:
                if char == quote_char:
                    # End of quoted string
                    in_quotes = False
                    quote_char = None
                else:
                    # Character inside quotes
                    current_arg += char

            i += 1

        # Add the last argument if there is one
        if current_arg:
            args.append(current_arg)

        return args

    @classmethod
    def from_str(cls, command: str, **kwargs) -> 'AsyncCommand':
        """
        Create a shell command.

        Args:
            command: Shell command string
            **kwargs: Additional arguments for AsyncCommand

        Returns:
            AsyncCommand: Configured command instance
        """
        kwargs['command_type'] = kwargs.get('command_type', CommandType.CLI)
        if '"' in command or "'" in command:
            cls.logger.warning(
                "Command '%s' contains quotes which can lead to the command failing due to parsing. It is recommended to build explicitly using the constructor to be able to escape the quotes correctly.",
                    command)
        return cls(
            args=AsyncCommand._parse_command_string(command),
            **kwargs
        )

    @classmethod
    def cmd(cls, command: str, **kwargs) -> 'AsyncCommand':
        """Create a Windows CMD command with proper argument handling."""
        stripped_command = command.strip()
        # For cmd, we pass the command directly to /c without additional quoting
        # The command will be parsed by cmd.exe itself
        args = ["cmd", "/c", stripped_command]
        return cls(args, **kwargs)

    @classmethod
    def powershell(cls, command: str, **kwargs) -> 'AsyncCommand':
        """Create a PowerShell command with proper argument handling."""
        stripped_command = command.strip()
        # For PowerShell, we pass the command directly to -Command without additional quoting
        # PowerShell will handle the command parsing internally
        args = ["powershell", "-Command", stripped_command]
        return cls(args, **kwargs)

    @classmethod
    def wsl(cls, command: str, **kwargs) -> 'AsyncCommand':
        """Create a WSL command with proper argument handling."""
        stripped_command = command.strip()
        # For WSL, we pass the command directly to bash -c
        args = ["wsl", "bash", "-c", stripped_command]
        return cls(args, **kwargs)

    def __await__(self):
        """Make AsyncCommand awaitable by delegating to execute()."""
        return self.execute().__await__()

    def __repr__(self) -> str:
        """String representation of the command."""
        return f"AsyncCommand(args={self.args}, state={self._state.value})"


class CommonCommands:
    @staticmethod
    def kill_pid(pid: int, **kwargs) -> 'AsyncCommand':
        return AsyncCommand.powershell(f'taskkill /PID {pid} /F', **kwargs)


__all__ = [
    "CommandResult",
    "CommandResponse",
    "CommandState",
    "CommandType",
    "CommandExecutionResult",
    "AsyncCommand",
    "CommonCommands"
]
