"""
Level 1 - Basic Functionality Tests

These tests cover the most fundamental aspects of AsyncCommand:
- Command initialization and basic properties
- Simple successful execution
- Basic result properties

If these tests fail, nothing else will work properly.
"""

import tempfile
from pathlib import Path

from danielutils import AsyncCommand, CommandType, CommandState
from .base import BaseCommandTest


class TestLevel1Basic(BaseCommandTest):
    """Level 1: Basic functionality tests."""

    def test_01_command_initialization_defaults(self) -> None:
        """Test command initialization with default parameters."""
        cmd = AsyncCommand.cmd("echo test")

        # Verify basic properties
        self.assertEqual(['cmd', '/c', 'echo test'], cmd.args)
        self.assertEqual(cmd.command_type, CommandType.CLI)
        self.assertIsNone(cmd.timeout)
        self.assertIsNone(cmd.cwd)
        self.assertEqual(cmd.env, {})
        self.assertIsNone(cmd.on_start)
        self.assertIsNone(cmd.on_complete)
        self.assertIsNone(cmd.on_error)

        # Verify initial state
        self.assertEqual(cmd.state, CommandState.PENDING)
        self.assertFalse(cmd.is_running)
        self.assertFalse(cmd.is_completed)
        self.assertIsNone(cmd.result)

    def test_02_command_initialization_with_parameters(self) -> None:
        """Test command initialization with custom parameters."""
        with tempfile.TemporaryDirectory() as temp_dir:
            def dummy_callback(cmd): pass

            cmd = AsyncCommand.cmd(
                "echo test",
                command_type=CommandType.GUI,
                timeout=5.0,
                cwd=temp_dir,
                env={'TEST_VAR': 'test_value'},
                on_start=dummy_callback,
                on_complete=dummy_callback,
                on_error=dummy_callback
            )

            # Verify all parameters are set correctly
            self.assertEqual(['cmd', '/c', 'echo test'], cmd.args)
            self.assertEqual(cmd.command_type, CommandType.GUI)
            self.assertEqual(cmd.timeout, 5.0)
            self.assertEqual(cmd.cwd, Path(temp_dir))
            self.assertEqual(cmd.env, {'TEST_VAR': 'test_value'})
            self.assertIsNotNone(cmd.on_start)
            self.assertIsNotNone(cmd.on_complete)
            self.assertIsNotNone(cmd.on_error)

    def test_03_command_properties(self) -> None:
        """Test command property access."""
        cmd = AsyncCommand.cmd("echo test")

        # Test state properties
        self.assertEqual(cmd.state, CommandState.PENDING)
        self.assertFalse(cmd.is_running)
        self.assertFalse(cmd.is_completed)
        self.assertIsNone(cmd.result)

        # Test string representation
        repr_str = repr(cmd)
        self.assertIn('AsyncCommand', repr_str)
        self.assertIn("['cmd', '/c', 'echo test']", repr_str)
        self.assertIn('pending', repr_str)

    def test_04_simple_successful_execution(self) -> None:
        """Test simple successful command execution."""
        cmd = AsyncCommand.cmd('echo Hello World')
        result = self.run_async(cmd.execute())

        # Verify execution was successful
        self.assertEqual(result.state, CommandState.COMPLETED)
        self.assertTrue(result.success)
        self.assertEqual(result.return_code, 0)
        self.assertIn('Hello World', result.stdout)
        self.assertEqual(result.stderr, '')
        self.assertGreater(result.execution_time, 0)
        self.assertIsNotNone(result.pid)
        self.assertEqual(result.command, cmd)
        self.assertEqual(result.command_type, CommandType.CLI)
        self.assertFalse(result.killed)
        self.assertFalse(result.timeout_occurred)
        self.assertIsNone(result.exception)

    def test_05_command_execution_result_properties(self) -> None:
        """Test CommandExecutionResult properties and methods."""
        cmd = AsyncCommand.cmd('echo test')
        result = self.run_async(cmd.execute())

        # Test basic properties
        self.assertTrue(result.success)
        self.assertEqual(result.return_code, 0)
        self.assertIn('test', result.stdout)
        self.assertEqual(result.command, cmd)

        # Test string representation
        str_repr = str(result)
        self.assertIn('CommandExecutionResult', str_repr)
        self.assertIn('SUCCESS', str_repr)
        self.assertIn('test', str_repr)

    def test_06_shell_command_factory(self) -> None:
        """Test shell command factory method."""
        cmd = AsyncCommand.cmd('echo Hello World')

        # Verify factory creates correct command
        self.assertEqual(['cmd', '/c', 'echo Hello World'], cmd.args)
        self.assertEqual(cmd.command_type, CommandType.CLI)

        # Test execution
        result = self.run_async(cmd.execute())
        self.assert_command_success(result, 'Hello World')

    def test_07_command_with_working_directory(self) -> None:
        """Test command execution with working directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            cmd = AsyncCommand(
                ['cmd', '/c', 'echo', '%CD%'],
                cwd=temp_dir
            )
            result = self.run_async(cmd.execute())

            # Verify command executed in correct directory
            self.assert_command_success(result)
            self.assertIn(temp_dir, result.stdout)

    def test_08_command_with_environment_variables(self) -> None:
        """Test command execution with environment variables."""
        cmd = AsyncCommand(
            ['cmd', '/c', 'echo', '%TEST_VAR%'],
            env={'TEST_VAR': 'test_value'}
        )
        result = self.run_async(cmd.execute())

        # Verify environment variable was passed correctly
        self.assert_command_success(result, 'test_value')

    def test_09_command_execution_failure(self) -> None:
        """Test command execution failure."""
        cmd = AsyncCommand(['nonexistent_command_12345'])
        result = self.run_async(cmd.execute())

        # Verify execution failed as expected
        self.assertEqual(result.state, CommandState.FAILED)
        self.assertFalse(result.success)
        self.assertNotEqual(result.return_code, 0)
        self.assertIsNotNone(result.stderr)
        self.assertEqual(result.command, cmd)
        self.assertFalse(result.killed)
        self.assertFalse(result.timeout_occurred)

    def test_10_command_state_after_execution(self) -> None:
        """Test command state after execution."""
        cmd = AsyncCommand.cmd('echo test')

        # Before execution
        self.assertEqual(cmd.state, CommandState.PENDING)
        self.assertFalse(cmd.is_running)
        self.assertFalse(cmd.is_completed)
        self.assertIsNone(cmd.result)

        # After execution
        result = self.run_async(cmd.execute())

        self.assertEqual(cmd.state, CommandState.COMPLETED)
        self.assertFalse(cmd.is_running)
        self.assertTrue(cmd.is_completed)
        self.assertEqual(cmd.result, result)


__all__ = [
    "TestLevel1Basic"
]
