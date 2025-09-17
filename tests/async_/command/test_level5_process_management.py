"""
Level 5: Process Management Tests

This module contains tests for advanced process management scenarios including:
- Process listing and identification
- Process creation and verification
- Process termination and cleanup
"""

import asyncio
import time
import tempfile
from typing import Set

from danielutils import AsyncCommand, CommandType, CommandState
from .base import BaseCommandTest
from .process_kill_context import CalculatorKillContext


class TestLevel5ProcessManagement(BaseCommandTest):
    """Level 5: Process management and advanced scenarios tests."""

    def setUp(self) -> None:
        if not hasattr(asyncio, "to_thread"):
            self.skipTest("asyncio.to_thread is not available")

    def _get_calculator_pids(self) -> Set[int]:
        """Get list of currently running calculator process PIDs."""
        try:
            # Use tasklist to find calculator processes
            cmd = AsyncCommand.powershell('tasklist /FI \"IMAGENAME eq CalculatorApp.exe\" /FO CSV')
            result = self.run_async(cmd.execute())

            if not result.success:
                return []

            # Parse the CSV output to extract PIDs
            pids = []
            lines = result.stdout.strip().split('\n')

            for line in lines[1:]:  # Skip header
                if 'calculatorapp.exe' in line.lower():
                    # CSV format: "Image Name","PID","Session Name","Session#","Mem Usage"
                    parts = line.split('","')
                    if len(parts) >= 2:
                        try:
                            pid = int(parts[1].strip('"'))
                            pids.append(pid)
                        except (ValueError, IndexError):
                            continue

            return set(pids)

        except Exception as e:
            self.logger.warning(f"Failed to get calculator PIDs: {e}")
            return set()

    def test_61_calculator_process_lifecycle_management(self) -> None:
        """Test complete calculator process lifecycle: list -> create -> verify -> kill -> verify."""

        with CalculatorKillContext(self) as ctx:
            calc_cmd = AsyncCommand(['calc'], command_type=CommandType.GUI)
            result = self.run_async(calc_cmd.execute())
            self.assertEqual(result.state, CommandState.COMPLETED)
            self.assertTrue(result.success)
            self.assertIsNotNone(result.pid)
            current_pids = ctx.get_app_pids()
            self.assertEqual(len(ctx.initial_pids) + 1, len(current_pids))

    def test_62_multiple_calculator_processes_management(self) -> None:
        """Test managing multiple calculator processes simultaneously."""

        with CalculatorKillContext(self) as ctx:
            # Create 3 calculator processes
            for _ in range(3):
                cmd = AsyncCommand(['calc'], command_type=CommandType.GUI)
                result = self.run_async(cmd.execute())

                self.assertEqual(result.state, CommandState.COMPLETED)
                self.assertTrue(result.success)
                self.assertIsNotNone(result.pid)

                # Small delay between creations
                time.sleep(0.5)

            # Verify we have 3 more processes than initially
            current_pids = ctx.get_app_pids()
            self.assertEqual(len(ctx.initial_pids) + 3, len(current_pids))

    def test_63_process_state_transitions_during_lifecycle(self) -> None:
        """Test command state transitions during process lifecycle."""

        with CalculatorKillContext(self) as ctx:
            cmd = AsyncCommand(['calc'], command_type=CommandType.GUI)

            # Initial state should be PENDING
            self.assertEqual(cmd.state, CommandState.PENDING)

            # Start execution
            result = self.run_async(cmd.execute())

            # After execution, state should be COMPLETED
            self.assertEqual(cmd.state, CommandState.COMPLETED)
            self.assertEqual(result.state, CommandState.COMPLETED)

            # State should still be COMPLETED (killing doesn't change execution state)
        self.assertEqual(cmd.state, CommandState.COMPLETED)

    def test_64_process_cleanup_and_error_handling(self) -> None:
        """Test process cleanup and error handling scenarios."""

        # Test killing a non-existent process
        fake_cmd = AsyncCommand(['calc'], command_type=CommandType.GUI)
        fake_cmd._process = None  # Simulate no process

        kill_result = fake_cmd.kill()
        self.assertFalse(kill_result)

        # Test process creation and automatic cleanup
        with CalculatorKillContext(self) as ctx:
            cmd = AsyncCommand(['calc'], command_type=CommandType.GUI)
            result = self.run_async(cmd.execute())

            # Verify it started successfully
            self.assertEqual(result.state, CommandState.COMPLETED)
            self.assertTrue(result.success)

            # Verify we have one more process than initially
            current_pids = ctx.get_app_pids()
            self.assertEqual(len(ctx.initial_pids) + 1, len(current_pids))

    def test_65_process_performance_and_timing(self) -> None:
        """Test process management performance and timing."""

        with CalculatorKillContext(self) as ctx:
            start_time = time.time()

            # Create calculator
            cmd = AsyncCommand(['calc'], command_type=CommandType.GUI)
            result = self.run_async(cmd.execute())

            creation_time = time.time() - start_time

            # Verify creation was fast (GUI commands should return quickly)
            self.assertLess(creation_time, 5.0)  # Should be much faster than 5 seconds

            # Verify we have one more process than initially
            current_pids = ctx.get_app_pids()
            self.assertEqual(len(ctx.initial_pids) + 1, len(current_pids))

            total_time = time.time() - start_time
            self.logger.info(f"Process lifecycle timing - Creation: {creation_time:.2f}s, Total: {total_time:.2f}s")

    def test_66_process_environment_and_working_directory(self) -> None:
        """Test process creation with custom environment and working directory."""

        with CalculatorKillContext(self) as ctx:
            with tempfile.TemporaryDirectory() as temp_dir:
                # Create calculator with custom working directory
                cmd = AsyncCommand(
                    ['calc'],
                    command_type=CommandType.GUI,
                    cwd=temp_dir,
                    env={'TEST_VAR': 'calc_test'}
                )

                result = self.run_async(cmd.execute())

                # Verify it started successfully
                self.assertEqual(result.state, CommandState.COMPLETED)
                self.assertTrue(result.success)

                # Verify we have one more process than initially
                current_pids = ctx.get_app_pids()
                self.assertEqual(len(ctx.initial_pids) + 1, len(current_pids))

    def test_67_process_callback_integration(self) -> None:
        """Test process callbacks during lifecycle management."""

        with CalculatorKillContext(self) as ctx:
            callbacks_called = []

            def start_callback(cmd, result=None):
                callbacks_called.append('start')

            def complete_callback(cmd, result=None):
                callbacks_called.append('complete')

            def error_callback(cmd, exception):
                callbacks_called.append('error')

            # Create calculator with callbacks
            cmd = AsyncCommand(
                ['calc'],
                command_type=CommandType.GUI,
                on_start=start_callback,
                on_complete=complete_callback,
                on_error=error_callback
            )

            result = self.run_async(cmd.execute())

            # Verify callbacks were called
            self.assertIn('start', callbacks_called)
            self.assertIn('complete', callbacks_called)
            self.assertNotIn('error', callbacks_called)

            # Verify we have one more process than initially
            current_pids = ctx.get_app_pids()
            self.assertEqual(len(ctx.initial_pids) + 1, len(current_pids))

    def test_68_process_timeout_handling(self) -> None:
        """Test process timeout handling for GUI commands."""

        with CalculatorKillContext(self) as ctx:
            # Create calculator with very short timeout
            cmd = AsyncCommand(
                ['calc'],
                command_type=CommandType.GUI,
                timeout=1  # Very short timeout
            )

            result = self.run_async(cmd.execute())

            # GUI commands should complete immediately regardless of timeout
            # because they don't wait for the process to finish
            self.assertEqual(CommandState.COMPLETED, result.state, result.stderr)
            self.assertTrue(result.success)

            # Verify we have one more process than initially
            current_pids = ctx.get_app_pids()
            self.assertEqual(len(ctx.initial_pids) + 1, len(current_pids))

    def test_69_process_concurrent_management(self) -> None:
        """Test concurrent process management scenarios."""

        with CalculatorKillContext(self) as ctx:
            # Start multiple processes
            for _ in range(2):
                cmd = AsyncCommand(['calc'], command_type=CommandType.GUI)
                result = self.run_async(cmd.execute())

                self.assertEqual(result.state, CommandState.COMPLETED)
                self.assertTrue(result.success)

            # Verify we have 2 more processes than initially
            current_pids = ctx.get_app_pids()
            self.assertEqual(len(ctx.initial_pids) + 2, len(current_pids))

    def test_70_comprehensive_process_management_integration(self) -> None:
        """Comprehensive integration test for process management."""

        with CalculatorKillContext(self) as ctx:
            # Process 1: Basic calculator
            cmd1 = AsyncCommand(['calc'], command_type=CommandType.GUI)
            result1 = self.run_async(cmd1.execute())
            self.assertEqual(result1.state, CommandState.COMPLETED)
            self.assertTrue(result1.success)

            # Process 2: Calculator with custom working directory
            with tempfile.TemporaryDirectory() as temp_dir:
                cmd2 = AsyncCommand(['calc'], command_type=CommandType.GUI, cwd=temp_dir)
                result2 = self.run_async(cmd2.execute())
                self.assertEqual(result2.state, CommandState.COMPLETED)
                self.assertTrue(result2.success)

            # Process 3: Calculator with environment variables
            cmd3 = AsyncCommand(
                ['calc'],
                command_type=CommandType.GUI,
                env={'PROCESS_TEST': 'integration_test'}
            )
            result3 = self.run_async(cmd3.execute())
            self.assertEqual(result3.state, CommandState.COMPLETED)
            self.assertTrue(result3.success)

            # Verify we have 3 more processes than initially
            current_pids = ctx.get_app_pids()
            self.assertEqual(len(ctx.initial_pids) + 3, len(current_pids))

            # Test process states
            self.assertEqual(cmd1.state, CommandState.COMPLETED)
            self.assertEqual(cmd2.state, CommandState.COMPLETED)
            self.assertEqual(cmd3.state, CommandState.COMPLETED)

    def test_71_concurrent_async_command_execution(self) -> None:
        """Test concurrent execution of multiple AsyncCommand instances using asyncio.gather."""

        with CalculatorKillContext(self) as ctx:
            # Create multiple AsyncCommand instances
            commands = [
                AsyncCommand(['calc'], command_type=CommandType.GUI),
                AsyncCommand(['calc'], command_type=CommandType.GUI),
                AsyncCommand(['calc'], command_type=CommandType.GUI)
            ]

            # Execute all commands concurrently using asyncio.gather
            async def run_commands():
                tasks = [cmd.execute() for cmd in commands]
                return await asyncio.gather(*tasks)

            results = self.run_async(run_commands())

            # Verify all commands completed successfully
            self.assertEqual(len(results), 3)
            for i, result in enumerate(results):
                self.assertEqual(result.state, CommandState.COMPLETED, f"Command {i} failed: {result.stderr}")
                self.assertTrue(result.success, f"Command {i} was not successful")
                self.assertIsNotNone(result.pid, f"Command {i} has no PID")

            # Verify all command objects have correct state
            for i, cmd in enumerate(commands):
                self.assertEqual(cmd.state, CommandState.COMPLETED, f"Command object {i} state is not COMPLETED")
                self.assertTrue(cmd.result.success, f"Command object {i} success is not True")

            # Verify we have 3 more processes than initially
            current_pids = ctx.get_app_pids()
            self.assertEqual(len(ctx.initial_pids) + 3, len(current_pids))

            # Verify all PIDs are unique
            result_pids = [result.pid for result in results]
            self.assertEqual(len(set(result_pids)), 3, "All PIDs should be unique")
