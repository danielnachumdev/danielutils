"""
Level 3 - Advanced Features Tests

These tests cover advanced functionality that builds on core features:
- Timeout handling
- Process management (kill, wait)
- State transitions and consistency
- Multiple executions

These tests assume Level 1 and Level 2 tests pass.
"""

import tempfile

from danielutils import AsyncCommand, CommandType, CommandState, CommandExecutionResult
from .base import BaseCommandTest


class TestLevel3Advanced(BaseCommandTest):
    """Level 3: Advanced features tests."""

    def test_24_command_timeout_handling(self) -> None:
        """Test command timeout handling."""
        cmd = AsyncCommand(
            ['ping', '127.0.0.1', '-n', '100'],
            timeout=0.1
        )
        result = self.run_async(cmd.execute())

        # Verify timeout occurred
        self.assertEqual(result.state, CommandState.TIMEOUT)
        self.assertFalse(result.success)
        self.assertTrue(result.timeout_occurred)
        self.assertFalse(result.killed)
        self.assertIsNotNone(result.pid)

    def test_25_command_timeout_with_callback(self) -> None:
        """Test command timeout with callback."""
        timeout_called = False
        timeout_command = None
        timeout_result = None

        def complete_callback(cmd, result):
            nonlocal timeout_called, timeout_command, timeout_result
            timeout_called = True
            timeout_command = cmd
            timeout_result = result

        cmd = AsyncCommand(
            ['ping', '127.0.0.1', '-n', '100'],
            timeout=0.1,
            on_complete=complete_callback
        )
        result = self.run_async(cmd.execute())

        # Verify timeout callback was called
        self.assertTrue(timeout_called)
        self.assertEqual(timeout_command, cmd)
        self.assertEqual(timeout_result, result)

        # Verify timeout occurred
        self.assertEqual(result.state, CommandState.TIMEOUT)
        self.assertTrue(result.timeout_occurred)

    def test_26_command_wait_functionality(self) -> None:
        """Test command wait functionality."""
        cmd = AsyncCommand.cmd("echo test")

        # Wait for pending command (should execute it)
        result = self.run_async(cmd.wait())

        # Verify command was executed and completed
        self.assert_command_success(result)
        self.assertEqual(cmd.state, CommandState.COMPLETED)

    def test_27_command_wait_already_completed(self) -> None:
        """Test waiting for already completed command."""
        cmd = AsyncCommand.cmd("echo test")

        # Execute command first
        result1 = self.run_async(cmd.execute())
        self.assert_command_success(result1)

        # Wait for already completed command
        result2 = self.run_async(cmd.wait())

        # Should return the same result
        self.assertEqual(result1, result2)
        self.assertEqual(cmd.state, CommandState.COMPLETED)

    def test_28_command_kill_not_running(self) -> None:
        """Test killing a command that is not running."""
        cmd = AsyncCommand.cmd("echo test")

        # Try to kill pending command
        killed = cmd.kill()

        # Should not be able to kill pending command
        self.assertFalse(killed)
        self.assertEqual(cmd.state, CommandState.PENDING)

    def test_29_command_kill_after_completion(self) -> None:
        """Test killing a command after it has completed."""
        cmd = AsyncCommand.cmd("echo test")

        # Execute command
        result = self.run_async(cmd.execute())
        self.assert_command_success(result)

        # Try to kill completed command
        killed = cmd.kill()

        # Should not be able to kill completed command
        self.assertFalse(killed)
        self.assertEqual(cmd.state, CommandState.COMPLETED)

    def test_30_command_state_transitions(self) -> None:
        """Test command state transitions during execution."""
        cmd = AsyncCommand.cmd("echo test")

        # Initial state
        self.assertEqual(cmd.state, CommandState.PENDING)
        self.assertFalse(cmd.is_running)
        self.assertFalse(cmd.is_completed)

        # Execute command
        result = self.run_async(cmd.execute())

        # Final state
        self.assertEqual(cmd.state, CommandState.COMPLETED)
        self.assertFalse(cmd.is_running)
        self.assertTrue(cmd.is_completed)
        self.assertEqual(cmd.result, result)

    def test_31_command_multiple_executions(self) -> None:
        """Test multiple executions of the same command."""
        cmd = AsyncCommand.cmd("echo test")

        # First execution
        result1 = self.run_async(cmd.execute())
        self.assert_command_success(result1)
        self.assertEqual(cmd.state, CommandState.COMPLETED)

        # Reset command state (simulate new command)
        cmd._state = CommandState.PENDING
        cmd._result = None
        cmd._process = None

        # Second execution
        result2 = self.run_async(cmd.execute())
        self.assert_command_success(result2)
        self.assertEqual(cmd.state, CommandState.COMPLETED)

        # Results should be different instances
        self.assertNotEqual(result1, result2)
        self.assertNotEqual(result1.pid, result2.pid)

    def test_32_command_execution_with_long_running_process(self) -> None:
        """Test command execution with a long-running process."""
        cmd = AsyncCommand(
            ['ping', '127.0.0.1', '-n', '5'],
            timeout=2.0
        )
        result = self.run_async(cmd.execute())

        # Should timeout due to short timeout
        self.assertEqual(result.state, CommandState.TIMEOUT)
        self.assertFalse(result.success)
        self.assertTrue(result.timeout_occurred)
        self.assertFalse(result.killed)

    def test_33_command_execution_with_very_short_timeout(self) -> None:
        """Test command execution with very short timeout."""
        cmd = AsyncCommand(
            ['ping', '127.0.0.1', '-n', '100'],
            timeout=0.01
        )
        result = self.run_async(cmd.execute())

        # Should timeout very quickly
        self.assertEqual(result.state, CommandState.TIMEOUT)
        self.assertFalse(result.success)
        self.assertTrue(result.timeout_occurred)
        self.assertLess(result.execution_time, 1.0)

    def test_34_command_execution_with_no_timeout(self) -> None:
        """Test command execution with no timeout."""
        cmd = AsyncCommand(
            ['ping', '127.0.0.1', '-n', '3']
        )
        result = self.run_async(cmd.execute())

        # Should complete successfully
        self.assertEqual(result.state, CommandState.COMPLETED)
        self.assertTrue(result.success)
        self.assertFalse(result.timeout_occurred)
        self.assertFalse(result.killed)

    def test_35_command_execution_with_environment_and_timeout(self) -> None:
        """Test command execution with environment variables and timeout."""
        cmd = AsyncCommand.cmd(
            "echo %TEST_VAR%",
            env={'TEST_VAR': 'timeout_test'},
            timeout=1.0
        )
        result = self.run_async(cmd.execute())

        # Should complete successfully with environment variable
        self.assert_command_success(result, 'timeout_test')
        self.assertFalse(result.timeout_occurred)

    def test_36_command_execution_with_cwd_and_timeout(self) -> None:
        """Test command execution with working directory and timeout."""
        with tempfile.TemporaryDirectory() as temp_dir:
            cmd = AsyncCommand.cmd(
                "echo %CD%",
                cwd=temp_dir,
                timeout=1.0
            )
            result = self.run_async(cmd.execute())

            # Should complete successfully in correct directory
            self.assert_command_success(result)
            self.assertIn(temp_dir, result.stdout)
            self.assertFalse(result.timeout_occurred)

    def test_37_command_execution_with_all_callbacks_and_timeout(self) -> None:
        """Test command execution with all callbacks and timeout."""
        callbacks_called = []

        def start_callback(cmd):
            callbacks_called.append('start')

        def complete_callback(cmd, result):
            callbacks_called.append('complete')

        def error_callback(cmd, exception):
            callbacks_called.append('error')

        cmd = AsyncCommand.cmd(
            "echo callback_test",
            timeout=1.0,
            on_start=start_callback,
            on_complete=complete_callback,
            on_error=error_callback
        )
        result = self.run_async(cmd.execute())

        # Verify callbacks were called in correct order
        self.assertEqual(callbacks_called, ['start', 'complete'])
        self.assert_command_success(result, 'callback_test')

    def test_38_command_execution_with_gui_and_timeout(self) -> None:
        """Test GUI command execution with timeout."""
        cmd = AsyncCommand.cmd(
            "echo GUI timeout test",
            command_type=CommandType.GUI,
            timeout=1.0
        )
        result = self.run_async(cmd.execute())

        # Should complete successfully
        self.assertEqual(result.state, CommandState.COMPLETED)
        self.assertTrue(result.success)
        self.assertEqual(result.command_type, CommandType.GUI)
        self.assertFalse(result.timeout_occurred)

    def test_39_command_state_consistency_during_execution(self) -> None:
        """Test that command state remains consistent during execution."""
        cmd = AsyncCommand.cmd("echo consistency_test")

        # Track state changes
        states = []

        def start_callback(cmd):
            states.append(('start', cmd.state))

        def complete_callback(cmd, result):
            states.append(('complete', cmd.state))

        cmd.on_start = start_callback
        cmd.on_complete = complete_callback

        result = self.run_async(cmd.execute())

        # Verify state consistency
        self.assertEqual(cmd.state, CommandState.COMPLETED)
        self.assertEqual(cmd.result, result)

        # Verify state transitions were recorded
        self.assertIn(('start', CommandState.RUNNING), states)
        self.assertIn(('complete', CommandState.COMPLETED), states)

    def test_40_command_execution_with_mixed_parameters_advanced(self) -> None:
        """Test command execution with all advanced parameters combined."""
        with tempfile.TemporaryDirectory() as temp_dir:
            callbacks_called = []

            def start_callback(cmd):
                callbacks_called.append('start')

            def complete_callback(cmd, result):
                callbacks_called.append('complete')

            def error_callback(cmd, exception):
                callbacks_called.append('error')

            cmd = AsyncCommand.cmd(
                "echo %TEST_VAR%",
                command_type=CommandType.CLI,
                timeout=2.0,
                cwd=temp_dir,
                env={'TEST_VAR': 'advanced_test'},
                on_start=start_callback,
                on_complete=complete_callback,
                on_error=error_callback
            )

            result = self.run_async(cmd.execute())

            # Verify all advanced features worked together
            self.assert_command_success(result, 'advanced_test')
            self.assertEqual(callbacks_called, ['start', 'complete'])
            self.assertIn(temp_dir, str(result.command.cwd))
            self.assertFalse(result.timeout_occurred)
            self.assertEqual(result.command_type, CommandType.CLI)


__all__ = [
    "TestLevel3Advanced"
]
