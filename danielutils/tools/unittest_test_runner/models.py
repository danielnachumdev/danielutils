"""
Data models for the test runner.
"""

from dataclasses import dataclass
from typing import List, Optional, Dict
import time


@dataclass
class TestFunctionState:
    """State of an individual test function."""
    function_name: str
    status: str  # "passed", "failed", "skipped", "error", "unknown"
    runtime: float
    timestamp: str
    error_message: str = ""
    warning_count: int = 0
    should_skip: bool = False
    skip_reason: str = ""
    improvement_from_initial: bool = False


@dataclass
class ModuleState:
    """State of a test module containing multiple test functions."""
    module_path: str
    test_functions: List[TestFunctionState]
    total_tests: int
    passed: int
    failed: int
    skipped: int
    errors: int
    total_runtime: float
    average_runtime: float
    slowest_test: str
    fastest_test: str
    success_rate: float
    timestamp: str
    should_skip_module: bool = False
    skip_reason: str = ""
    improvement_from_initial: bool = False


@dataclass
class TestResult:
    """Result of running a test module with initial and current states."""
    module_path: str
    initial_state: Optional[ModuleState]
    current_state: ModuleState
    errors: List[str]
    warnings: List[str]
    overall_improvement: bool = False


@dataclass
class TestRunSummary:
    """Summary of a complete test run across all modules."""
    timestamp: str
    python_executable: str
    total_modules: int
    modules_run: int
    modules_skipped: int
    total_tests: int
    total_passed: int
    total_failed: int
    total_skipped: int
    total_errors: int
    success_rate: float
    total_execution_time: float
    results: List[TestResult]


@dataclass
class TestDiscovery:
    """Represents discovered test structure for progress tracking."""
    modules: List[str]
    classes: Dict[str, List[str]]  # module -> list of classes
    functions: Dict[str, List[str]]  # class -> list of functions
    total_functions: int
    total_classes: int
    total_modules: int
