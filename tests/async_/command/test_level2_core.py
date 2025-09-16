"""
Level 2 - Core Features Tests

These tests cover core functionality that builds on basic features:
- Error handling and failure cases
- Environment variables and working directory
- Callbacks (start, complete, error)
- Command types (CLI vs GUI)

These tests assume Level 1 tests pass.
"""

import tempfile
from pathlib import Path

from danielutils import AsyncCommand, CommandType, CommandState, CommandExecutionResult
from .base import BaseCommandTest


class TestLevel2Core(BaseCommandTest):
    """Level 2: Core features tests."""

    def test_11_error_callback_execution(self) -> None:
        """Test error callback is called for failed commands."""
        error_called = False
        error_command = None
        error_exception = None

        def error_callback(cmd, exception):
            nonlocal error_called, error_command, error_exception
            error_called = True
            error_command = cmd
            error_exception = exception

        cmd = AsyncCommand(
            ['nonexistent_command_12345'],
            on_error=error_callback
        )
        result = self.run_async(cmd.execute())

        # Verify error callback was called
        self.assertTrue(error_called)
        self.assertEqual(error_command, cmd)
        self.assertIsNotNone(error_exception)

        # Verify command failed
        self.assert_command_failure(result)

    def test_12_success_callback_execution(self) -> None:
        """Test success callback is called for successful commands."""
        complete_called = False
        complete_command = None
        complete_result = None

        def complete_callback(cmd, result):
            nonlocal complete_called, complete_command, complete_result
            complete_called = True
            complete_command = cmd
            complete_result = result

        cmd = AsyncCommand.cmd("echo Hello World", on_complete=complete_callback)
        result = self.run_async(cmd.execute())

        # Verify complete callback was called
        self.assertTrue(complete_called)
        self.assertEqual(complete_command, cmd)
        self.assertEqual(complete_result, result)

        # Verify command succeeded
        self.assert_command_success(result, 'Hello World')

    def test_13_start_callback_execution(self) -> None:
        """Test start callback is called when command starts."""
        start_called = False
        start_command = None

        def start_callback(cmd):
            nonlocal start_called, start_command
            start_called = True
            start_command = cmd

        cmd = AsyncCommand.cmd("echo test", on_start=start_callback)
        result = self.run_async(cmd.execute())

        # Verify start callback was called
        self.assertTrue(start_called)
        self.assertEqual(start_command, cmd)

        # Verify command succeeded
        self.assert_command_success(result)

    def test_14_all_callbacks_execution(self) -> None:
        """Test all callbacks are called in correct order."""
        callbacks_called = []

        def start_callback(cmd):
            callbacks_called.append('start')

        def complete_callback(cmd, result):
            callbacks_called.append('complete')

        def error_callback(cmd, exception):
            callbacks_called.append('error')

        # Test successful command
        cmd = AsyncCommand.cmd(
            "echo test",
            on_start=start_callback,
            on_complete=complete_callback,
            on_error=error_callback
        )
        result = self.run_async(cmd.execute())

        # Verify only start and complete callbacks were called
        self.assertEqual(callbacks_called, ['start', 'complete'])
        self.assert_command_success(result)

    def test_15_gui_command_execution(self) -> None:
        """Test GUI command execution (no output capture)."""
        cmd = AsyncCommand.cmd("echo GUI Test", command_type=CommandType.GUI)
        result = self.run_async(cmd.execute())

        # Verify GUI command properties
        self.assertEqual(result.command_type, CommandType.GUI)
        self.assertEqual(result.stdout, '')  # GUI commands don't capture output
        self.assertEqual(result.stderr, '')  # GUI commands don't capture output
        self.assertIsNotNone(result.pid)
        self.assertGreater(result.execution_time, 0)

    def test_16_cli_vs_gui_command_types(self) -> None:
        """Test difference between CLI and GUI command types."""
        # CLI command
        cli_cmd = AsyncCommand.cmd("echo CLI Test", command_type=CommandType.CLI)
        cli_result = self.run_async(cli_cmd.execute())

        # GUI command
        gui_cmd = AsyncCommand.cmd("echo GUI Test", command_type=CommandType.GUI)
        gui_result = self.run_async(gui_cmd.execute())

        # Verify differences
        self.assertEqual(cli_result.command_type, CommandType.CLI)
        self.assertEqual(gui_result.command_type, CommandType.GUI)

        # CLI captures output, GUI doesn't
        self.assertIn('CLI Test', cli_result.stdout)
        self.assertEqual(gui_result.stdout, '')

    def test_17_environment_variables_complex(self) -> None:
        """Test complex environment variable scenarios."""
        env = {
            'VAR1': 'value1',
            'VAR2': 'value2',
            'PATH': 'custom_path'
        }

        cmd = AsyncCommand.cmd("echo %VAR1% %VAR2%", env=env)
        result = self.run_async(cmd.execute())

        # Verify environment variables were passed
        self.assert_command_success(result)
        self.assertIn('value1', result.stdout)
        self.assertIn('value2', result.stdout)

    def test_18_working_directory_complex(self) -> None:
        """Test complex working directory scenarios."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a test file in the directory
            test_file = Path(temp_dir) / 'test.txt'
            test_file.write_text('test content')

            cmd = AsyncCommand(
                ['cmd', '/c', 'type', 'test.txt'],
                cwd=temp_dir
            )
            result = self.run_async(cmd.execute())

            # Verify command executed in correct directory
            self.assert_command_success(result, 'test content')

    def test_19_command_with_timeout_parameter(self) -> None:
        """Test command with timeout parameter (not execution timeout)."""
        cmd = AsyncCommand.cmd("echo test", timeout=10.0)

        # Verify timeout parameter is set
        self.assertEqual(cmd.timeout, 10.0)

        # Execute command
        result = self.run_async(cmd.execute())
        self.assert_command_success(result)

    def test_20_command_execution_with_mixed_parameters(self) -> None:
        """Test command execution with all parameters combined."""
        with tempfile.TemporaryDirectory() as temp_dir:
            callbacks_called = []

            def start_callback(cmd):
                callbacks_called.append('start')

            def complete_callback(cmd, result):
                callbacks_called.append('complete')

            cmd = AsyncCommand.cmd(
                "echo %TEST_VAR%",
                command_type=CommandType.CLI,
                timeout=5.0,
                cwd=temp_dir,
                env={'TEST_VAR': 'mixed_test'},
                on_start=start_callback,
                on_complete=complete_callback
            )

            result = self.run_async(cmd.execute())

            # Verify all parameters worked together
            self.assert_command_success(result, 'mixed_test')
            self.assertEqual(callbacks_called, ['start', 'complete'])
            self.assertIn(temp_dir, str(result.command.cwd))

    def test_21_command_result_immutability(self) -> None:
        """Test that command result is immutable after execution."""
        cmd = AsyncCommand.cmd("echo test")
        result = self.run_async(cmd.execute())

        # Store original values
        original_success = result.success
        original_stdout = result.stdout
        original_stderr = result.stderr
        original_return_code = result.return_code

        # Verify result properties don't change
        self.assertEqual(result.success, original_success)
        self.assertEqual(result.stdout, original_stdout)
        self.assertEqual(result.stderr, original_stderr)
        self.assertEqual(result.return_code, original_return_code)

        # Verify command state is consistent
        self.assertEqual(cmd.state, CommandState.COMPLETED)
        self.assertEqual(cmd.result, result)

    def test_22_command_execution_with_empty_args(self) -> None:
        """Test command execution with empty arguments."""
        cmd = AsyncCommand([])
        result = self.run_async(cmd.execute())

        # Empty command should fail
        self.assertEqual(result.state, CommandState.FAILED)
        self.assertFalse(result.success)
        self.assertNotEqual(result.return_code, 0)

    def test_23_command_execution_with_whitespace_args(self) -> None:
        """Test command execution with whitespace-only arguments."""
        cmd = AsyncCommand(['   ', '\t', '\n'])
        result = self.run_async(cmd.execute())

        # Whitespace-only command should fail
        self.assertEqual(result.state, CommandState.FAILED)
        self.assertFalse(result.success)
        self.assertNotEqual(result.return_code, 0)


__all__ = [
    "TestLevel2Core"
]
