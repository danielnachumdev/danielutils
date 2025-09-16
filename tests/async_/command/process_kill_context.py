"""
Process Context Manager for Testing

This module provides a context manager for testing process lifecycle management.
It tracks PIDs before entering the context and cleans up any new processes on exit.
"""
import logging

import time
from typing import Set, List

from danielutils import AsyncCommand
from .base import BaseCommandTest


class ProcessKillContext:
    """
    Context manager for testing process lifecycle management.

    Tracks PIDs of a specific application before entering the context,
    and kills any new processes of that application when exiting.
    """

    def __init__(self, app_name: str, test_instance: BaseCommandTest):
        """
        Initialize the process context manager.

        Args:
            app_name: Name of the application to track (e.g., 'CalculatorApp.exe')
            test_instance: The test instance for running async commands
        """
        self.app_name = app_name
        self.test_instance = test_instance
        self.initial_pids: Set[int] = set()
        self.created_pids: List[int] = []
        self.logger = logging.getLogger(self.__class__.__name__)

    def get_app_pids(self) -> Set[int]:
        """Get list of currently running application process PIDs."""
        try:
            # Use tasklist to find application processes
            cmd = AsyncCommand(
                ["powershell", "-Command", "tasklist", "/FI", f"\"IMAGENAME eq {self.app_name}\"", "/FO", "CSV"])
            result = self.test_instance.run_async(cmd.execute())

            if not result.success:
                return set()

            # Parse the CSV output to extract PIDs
            pids = []
            lines = result.stdout.strip().split('\n')

            for line in lines[1:]:  # Skip header
                if self.app_name.lower() in line.lower():
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
            self.logger.warning(f"Failed to get {self.app_name} PIDs: {e}")
            return set()

    def _kill_pid(self, pid: int) -> bool:
        """Kill a specific process by PID."""
        try:
            kill_cmd = AsyncCommand.powershell(f'taskkill /PID {pid} /F')
            result = self.test_instance.run_async(kill_cmd.execute())
            return result.success
        except Exception as e:
            self.logger.warning(f"Failed to kill PID {pid}: {e}")
            return False

    def track_pid(self, pid: int) -> None:
        """Track a newly created PID for cleanup."""
        if pid not in self.initial_pids:
            self.created_pids.append(pid)

    def __enter__(self) -> 'ProcessKillContext':
        """Enter the context and record initial PIDs."""
        self.initial_pids = self.get_app_pids()
        self.logger.info(f"ProcessContext: Initial {self.app_name} PIDs: {self.initial_pids}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit the context and clean up any new processes."""
        # Give processes a moment to fully start
        time.sleep(0.5)

        # Get current PIDs
        current_pids = self.get_app_pids()
        self.logger.info(f"ProcessContext: Current {self.app_name} PIDs: {current_pids}")
        new_pids = current_pids - self.initial_pids

        # Add any tracked PIDs that might not be in current_pids yet
        for pid in self.created_pids:
            if pid not in current_pids:
                new_pids.add(pid)

        self.logger.info(f"ProcessContext: Cleaning up {len(new_pids)} new {self.app_name} processes: {new_pids}")

        # Kill all new processes
        for pid in new_pids:
            self._kill_pid(pid)
            time.sleep(0.1)  # Small delay between kills

        # Final cleanup - check again and kill any remaining
        time.sleep(1)
        final_pids = self.get_app_pids()
        remaining_new = final_pids - self.initial_pids

        if remaining_new:
            self.logger.warning(
                f"ProcessContext: {len(remaining_new)} processes still running after cleanup: {remaining_new}")
            for pid in remaining_new:
                self._kill_pid(pid)


class CalculatorKillContext(ProcessKillContext):
    def __init__(self, test_instance: BaseCommandTest) -> None:
        super().__init__('CalculatorApp.exe', test_instance)


__all__ = [
    "ProcessKillContext",
    "CalculatorKillContext",
]
