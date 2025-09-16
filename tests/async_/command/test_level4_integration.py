"""
Level 4 - Integration & Edge Cases Tests

These tests cover complex scenarios combining multiple features:
- Complex scenarios combining multiple features
- Edge cases and error conditions
- Performance and reliability
- Stress testing

These tests assume Level 1, 2, and 3 tests pass.
"""

import tempfile
import time
from pathlib import Path

from danielutils import AsyncCommand, CommandType, CommandState, CommandExecutionResult
from .base import BaseCommandTest


class TestLevel4Integration(BaseCommandTest):
    """Level 4: Integration and edge cases tests."""

    def test_41_multiple_commands_sequential_execution(self) -> None:
        """Test executing multiple commands sequentially."""
        commands = [
            AsyncCommand.cmd("echo First"),
            AsyncCommand.cmd("echo Second"),
            AsyncCommand.cmd("echo Third")
        ]

        results = []
        for cmd in commands:
            result = self.run_async(cmd.execute())
            results.append(result)
            self.assert_command_success(result)

        # Verify all commands executed successfully
        self.assertEqual(len(results), 3)
        self.assertIn('First', results[0].stdout)
        self.assertIn('Second', results[1].stdout)
        self.assertIn('Third', results[2].stdout)

    def test_42_multiple_commands_with_different_parameters(self) -> None:
        """Test executing multiple commands with different parameters."""
        with tempfile.TemporaryDirectory() as temp_dir:
            commands = [
                AsyncCommand.cmd("echo Basic", command_type=CommandType.CLI),
                AsyncCommand.cmd("echo GUI", command_type=CommandType.GUI),
                AsyncCommand.cmd("echo %TEST_VAR%", env={'TEST_VAR': 'env_test'}),
                AsyncCommand.cmd("echo %CD%", cwd=temp_dir),
                AsyncCommand.cmd("echo Timeout", timeout=1.0)
            ]

            results = []
            for cmd in commands:
                result = self.run_async(cmd.execute())
                results.append(result)
                self.assert_command_success(result)

            # Verify all commands executed with their specific parameters
            self.assertEqual(len(results), 5)
            self.assertEqual(results[0].command_type, CommandType.CLI)
            self.assertEqual(results[1].command_type, CommandType.GUI)
            self.assertIn('env_test', results[2].stdout)
            self.assertIn(temp_dir, results[3].stdout)
            self.assertIn('Timeout', results[4].stdout)

    def test_43_command_execution_with_complex_environment(self) -> None:
        """Test command execution with complex environment setup."""
        complex_env = {
            'VAR1': 'value1',
            'VAR2': 'value2',
            'VAR3': 'value3',
            'PATH': 'custom_path',
            'TEMP': 'custom_temp'
        }

        cmd = AsyncCommand.cmd("echo %VAR1% %VAR2% %VAR3%", env=complex_env)
        result = self.run_async(cmd.execute())

        # Verify all environment variables were passed
        self.assert_command_success(result)
        self.assertIn('value1', result.stdout)
        self.assertIn('value2', result.stdout)
        self.assertIn('value3', result.stdout)

    def test_44_command_execution_with_nested_directories(self) -> None:
        """Test command execution with nested directory structure."""
        with tempfile.TemporaryDirectory() as base_dir:
            # Create nested directory structure
            nested_dir = Path(base_dir) / 'level1' / 'level2' / 'level3'
            nested_dir.mkdir(parents=True, exist_ok=True)

            # Create test file in nested directory
            test_file = nested_dir / 'test.txt'
            test_file.write_text('nested test content')

            cmd = AsyncCommand(
                ['cmd', '/c', 'type', 'test.txt'],
                cwd=nested_dir
            )
            result = self.run_async(cmd.execute())

            # Verify command executed in nested directory
            self.assert_command_success(result, 'nested test content')

    def test_45_command_execution_with_special_characters(self) -> None:
        """Test command execution with special characters in arguments."""
        # cannot check here '^', '&' as they are special for cmd: & to execute
        # multiple commands and ^ as the escape char
        special_chars = ['!', '@', '#', '$', '%', '*', '(', ')', '[', ']', '{', '}']

        for char in special_chars:
            cmd = AsyncCommand.cmd(f"echo test{char}")
            result = self.run_async(cmd.execute())

            # Should handle special characters gracefully
            self.assert_command_success(result)
            self.assertIn(f'test{char}', result.stdout, f"Expected: test{char} but got {result.stdout}")

    def test_46_command_execution_with_unicode_characters(self) -> None:
        """Test command execution with unicode characters."""
        unicode_strings = ['Hello 世界', 'Привет мир', 'مرحبا بالعالم', '🌍🌎🌏']

        for unicode_str in unicode_strings:
            # Use PowerShell for better unicode support
            cmd = AsyncCommand.cmd(f'echo {unicode_str}')
            result = self.run_async(cmd.execute())

            # Should handle unicode characters
            self.assert_command_success(result)
            self.assertIn(unicode_str, result.stdout)

    def test_47_command_execution_with_very_long_arguments(self) -> None:
        """Test command execution with very long arguments."""
        long_string = 'A' * 1000  # 1000 character string

        cmd = AsyncCommand.cmd(f"echo {long_string}")
        result = self.run_async(cmd.execute())

        # Should handle long arguments
        self.assert_command_success(result)
        self.assertIn(long_string, result.stdout)

    def test_48_command_execution_with_empty_environment(self) -> None:
        """Test command execution with empty environment variables."""
        cmd = AsyncCommand.cmd("echo %NONEXISTENT_VAR%", env={}
                               )
        result = self.run_async(cmd.execute())

        # Should handle empty environment gracefully
        self.assert_command_success(result)
        self.assertIn('%NONEXISTENT_VAR%', result.stdout)

    def test_49_command_execution_with_nonexistent_directory(self) -> None:
        """Test command execution with nonexistent working directory."""
        nonexistent_dir = Path('/nonexistent/directory/that/does/not/exist')

        cmd = AsyncCommand.cmd("echo test", cwd=nonexistent_dir)
        result = self.run_async(cmd.execute())

        # Should fail gracefully with nonexistent directory
        self.assertEqual(result.state, CommandState.FAILED)
        self.assertFalse(result.success)
        self.assertNotEqual(result.return_code, 0)

    def test_50_command_execution_with_invalid_timeout(self) -> None:
        """Test command execution with invalid timeout values."""
        with self.assertRaises(ValueError):
            AsyncCommand.cmd("echo test", timeout=-1.0)
        with self.assertRaises(ValueError):
            AsyncCommand.cmd("echo test", timeout=0.0)

    def test_51_command_execution_stress_test(self) -> None:
        """Test command execution under stress (multiple rapid executions)."""
        commands = []
        for i in range(10):
            cmd = AsyncCommand.cmd(f"echo stress_test_{i}")
            commands.append(cmd)

        # Execute all commands rapidly
        results = []
        for cmd in commands:
            result = self.run_async(cmd.execute())
            results.append(result)

        # Verify all commands executed successfully
        self.assertEqual(len(results), 10)
        for i, result in enumerate(results):
            self.assert_command_success(result)
            self.assertIn(f'stress_test_{i}', result.stdout)

    def test_52_command_execution_with_concurrent_timeouts(self) -> None:
        """Test command execution with concurrent timeout scenarios."""
        # Create multiple commands with different timeouts
        commands = [
            AsyncCommand(['ping', '127.0.0.1', '-n', '100'], timeout=0.1),
            AsyncCommand(['ping', '127.0.0.1', '-n', '100'], timeout=0.2),
            AsyncCommand(['ping', '127.0.0.1', '-n', '100'], timeout=0.3)
        ]

        results = []
        for cmd in commands:
            result = self.run_async(cmd.execute())
            results.append(result)

        # All should timeout
        for result in results:
            self.assertEqual(result.state, CommandState.TIMEOUT)
            self.assertTrue(result.timeout_occurred)
            self.assertFalse(result.success)

    def test_53_command_execution_with_mixed_success_failure(self) -> None:
        """Test command execution with mixed success and failure scenarios."""
        commands = [
            AsyncCommand.cmd("echo success1"),
            AsyncCommand(['nonexistent_command_12345']),
            AsyncCommand.cmd("echo success2"),
            AsyncCommand(['another_nonexistent_command']),
            AsyncCommand.cmd("echo success3")
        ]

        results = []
        for cmd in commands:
            result = self.run_async(cmd.execute())
            results.append(result)

        # Verify mixed results
        self.assertEqual(len(results), 5)
        self.assert_command_success(results[0], 'success1')
        self.assert_command_failure(results[1])
        self.assert_command_success(results[2], 'success2')
        self.assert_command_failure(results[3])
        self.assert_command_success(results[4], 'success3')

    def test_54_command_execution_with_complex_callback_chains(self) -> None:
        """Test command execution with complex callback chains."""
        callback_chain = []

        def create_callback(name):
            def callback(cmd, result=None):
                callback_chain.append(name)

            return callback

        cmd = AsyncCommand.cmd(
            "echo callback_chain_test",
            on_start=create_callback('start'),
            on_complete=create_callback('complete'),
            on_error=create_callback('error')
        )

        result = self.run_async(cmd.execute())

        # Verify callback chain
        self.assertEqual(callback_chain, ['start', 'complete'])
        self.assert_command_success(result, 'callback_chain_test')

    def test_55_command_execution_with_edge_case_arguments(self) -> None:
        """Test command execution with edge case arguments."""
        edge_cases = [
            [],  # Empty arguments
            [''],  # Empty string argument
            ['   '],  # Whitespace only
            ['\t\n\r'],  # Various whitespace
            ['"quoted string"'],  # Quoted string
            ["'single quoted'"],  # Single quoted string
            ['arg1', '', 'arg3'],  # Mixed empty and non-empty
        ]

        for args in edge_cases:
            cmd = AsyncCommand(args)
            result = self.run_async(cmd.execute())

            # Should handle edge cases gracefully (may succeed or fail)
            self.assertIsInstance(result, CommandExecutionResult)
            self.assertIsNotNone(result.state)
            self.assertIsNotNone(result.success)
            self.assertIsNotNone(result.return_code)

    def test_56_command_execution_performance_benchmark(self) -> None:
        """Test command execution performance."""
        cmd = AsyncCommand.cmd("echo performance_test")

        # Measure execution time
        start_time = time.time()
        result = self.run_async(cmd.execute())
        end_time = time.time()

        execution_time = end_time - start_time

        # Should complete quickly
        self.assertLess(execution_time, 1.0)  # Should complete within 1 second
        self.assert_command_success(result, 'performance_test')

        # Verify internal execution time is reasonable
        self.assertLess(result.execution_time, 1.0)

    def test_57_command_execution_with_memory_stress(self) -> None:
        """Test command execution with memory stress (large output)."""
        # Create a command that produces large output
        large_output = 'A' * 10000  # 10KB output

        cmd = AsyncCommand.powershell(f"echo {large_output}")
        result = self.run_async(cmd.execute())

        # Should handle large output
        self.assert_command_success(result)
        self.assertIn(large_output, result.stdout)
        self.assertGreater(len(result.stdout), 10000)

    def test_58_command_execution_reliability_test(self) -> None:
        """Test command execution reliability (multiple executions of same command)."""
        cmd = AsyncCommand.cmd("echo reliability_test")

        # Execute the same command multiple times
        results = []
        for i in range(5):
            result = self.run_async(cmd.execute())
            results.append(result)

            # Reset command state for next execution
            cmd._state = CommandState.PENDING
            cmd._result = None
            cmd._process = None

        # All executions should succeed
        for result in results:
            self.assert_command_success(result, 'reliability_test')

    def test_59_command_execution_with_system_limits(self) -> None:
        """Test command execution with system limits."""
        # Test with very long command line
        large_output = 'A' * 1000  # 10KB output

        cmd = AsyncCommand.cmd(f"echo {large_output}")
        result = self.run_async(cmd.execute())

        # Should handle long command line
        self.assert_command_success(result)
        self.assertIn('A', result.stdout)

    def test_60_comprehensive_integration_test(self) -> None:
        """Comprehensive integration test combining all features."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test file
            test_file = Path(temp_dir) / 'integration_test.txt'
            test_file.write_text('integration test content')

            # Track all callbacks
            all_callbacks = []

            def track_callback(name):
                def callback(cmd, result=None):
                    all_callbacks.append(f"{name}_{'_'.join(cmd.args)}")

                return callback

            # Create complex command with all features
            cmd = AsyncCommand(
                args=['cmd', '/c', 'type', 'integration_test.txt'],
                command_type=CommandType.CLI,
                timeout=5.0,
                cwd=temp_dir,
                env={'INTEGRATION_TEST': 'true'},
                on_start=track_callback('start'),
                on_complete=track_callback('complete'),
                on_error=track_callback('error')
            )

            # Execute command
            result = self.run_async(cmd.execute())

            # Verify all features worked together
            self.assert_command_success(result, 'integration test content')
            self.assertEqual(result.command_type, CommandType.CLI)
            self.assertFalse(result.timeout_occurred)
            self.assertFalse(result.killed)
            self.assertIn(temp_dir, str(result.command.cwd))
            self.assertEqual(['start_cmd_/c_type_integration_test.txt', 'complete_cmd_/c_type_integration_test.txt'], all_callbacks)

            # Verify command state is consistent
            self.assertEqual(cmd.state, CommandState.COMPLETED)
            self.assertEqual(cmd.result, result)
            self.assertTrue(cmd.is_completed)
            self.assertFalse(cmd.is_running)


__all__ = [
    "TestLevel4Integration"
]
