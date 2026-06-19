"""
Base test class for Command tests.
"""

import subprocess
from typing import List, Optional, Any
from unittest.mock import patch, MagicMock

from danielutils import AsyncCommand, CommandType, CommandState, CommandExecutionResult
from tests.base import BaseTest


class BaseCommandTest(BaseTest):
    """Base test class for all Command tests."""

    def setUp(self) -> None:
        """Set up test fixtures before each test method."""
        super().setUp()
        self._created_commands: List = []

    def tearDown(self) -> None:
        """Clean up after each test method."""
        # Clean up any command processes
        if hasattr(self, '_created_commands'):
            for cmd in self._created_commands:
                if hasattr(cmd, 'cleanup'):
                    cmd.cleanup()
        super().tearDown()

    def create_simple_command(
            self,
            args: Optional[List[str]] = None,
            command_type: CommandType = CommandType.CLI,
            **kwargs: Any
    ) -> AsyncCommand:
        """Create a simple command for testing."""
        if args is None:
            # Use Windows-compatible command
            cmd = AsyncCommand.cmd("echo test", command_type=command_type, **kwargs)
        else:
            cmd = AsyncCommand(args, command_type=command_type, **kwargs)
        self._created_commands.append(cmd)
        return cmd

    def create_successful_command(self, **kwargs: Any) -> AsyncCommand:
        """Create a command that will succeed."""
        cmd = AsyncCommand.cmd("echo Hello World", **kwargs)
        self._created_commands.append(cmd)
        return cmd

    def create_failing_command(self, **kwargs: Any) -> AsyncCommand:
        """Create a command that will fail."""
        return self.create_simple_command(['nonexistent_command_12345'], **kwargs)

    def create_timeout_command(self, timeout: float = 0.1, **kwargs: Any) -> AsyncCommand:
        """Create a command that will timeout."""
        cmd = AsyncCommand.cmd("ping 127.0.0.1 -n 100", timeout=timeout, **kwargs)
        self._created_commands.append(cmd)
        return cmd

    def create_gui_command(self, **kwargs: Any) -> AsyncCommand:
        """Create a GUI command for testing."""
        return self.create_simple_command(['notepad'], command_type=CommandType.GUI, **kwargs)

    async def execute_command(self, command: AsyncCommand) -> CommandExecutionResult:
        """Execute a command and return the result."""
        return await command.execute()

    def assert_command_success(self, result: CommandExecutionResult, expected_output: Optional[str] = None) -> None:
        """Assert that a command result indicates success."""
        self.assertEqual(CommandState.COMPLETED, result.state, result.stderr)
        self.assertTrue(result.success)
        self.assertEqual(0, result.return_code)
        self.assertIsNotNone(result.pid)
        self.assertGreater(result.execution_time, 0)
        if expected_output:
            self.assertIn(expected_output, result.stdout)

    def assert_command_failure(self, result: CommandExecutionResult, expected_error: Optional[str] = None) -> None:
        """Assert that a command result indicates failure."""
        self.assertEqual(result.state, CommandState.FAILED)
        self.assertFalse(result.success)
        self.assertNotEqual(result.return_code, 0)  # Any non-zero return code indicates failure
        if expected_error:
            self.assertIn(expected_error, result.stderr.lower())

    def assert_command_timeout(self, result: CommandExecutionResult) -> None:
        """Assert that a command result indicates timeout."""
        self.assertEqual(result.state, CommandState.TIMEOUT)
        self.assertFalse(result.success)
        self.assertTrue(result.timeout_occurred)

    def assert_command_killed(self, result: CommandExecutionResult) -> None:
        """Assert that a command result indicates it was killed."""
        self.assertEqual(result.state, CommandState.KILLED)
        self.assertFalse(result.success)
        self.assertTrue(result.killed)

    def mock_subprocess_success(
            self,
            stdout: str = "test output",
            stderr: str = "",
            returncode: int = 0
    ) -> patch:
        """Mock subprocess.Popen to return a successful result."""
        mock_process: MagicMock = MagicMock()
        mock_process.pid = 12345
        mock_process.returncode = returncode
        mock_process.communicate.return_value = (stdout, stderr)
        mock_process.poll.return_value = returncode

        return patch('subprocess.Popen', return_value=mock_process)

    def mock_subprocess_failure(self, error_msg: str = "Test error") -> patch:
        """Mock subprocess.Popen to raise an exception."""
        return patch('subprocess.Popen', side_effect=OSError(error_msg))

    def mock_subprocess_timeout(self) -> patch:
        """Mock subprocess.Popen to timeout."""
        mock_process: MagicMock = MagicMock()
        mock_process.pid = 12345
        mock_process.communicate.side_effect = subprocess.TimeoutExpired('test', 1.0)
        mock_process.kill.return_value = None
        mock_process.returncode = -1

        return patch('subprocess.Popen', return_value=mock_process)


__all__ = [
    "BaseCommandTest"
]
