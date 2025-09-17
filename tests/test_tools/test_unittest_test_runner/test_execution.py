"""
Tests for the TestExecutor class.
"""
import unittest
from unittest.mock import patch, MagicMock, call
import subprocess

from danielutils.tools.unittest_test_runner.core.execution import TestExecutor
from danielutils.tools.unittest_test_runner.models import TestDiscovery, TestFunctionState
from tests.test_tools.base import BaseToolTest


class TestTestExecutor(BaseToolTest):
    """Test cases for TestExecutor."""
    
    def setUp(self):
        """Set up test fixtures."""
        super().setUp()
        self.python_path = "python"
        self.verbose = "class"
        
        self.test_discovery = TestDiscovery(
            modules=["tests.test_module"],
            classes={"tests.test_module": ["TestClass"]},
            functions={"tests.test_module.TestClass": ["test_function1", "test_function2"]},
            total_functions=2,
            total_classes=1,
            total_modules=1
        )
        self.executor = TestExecutor(self.python_path, self.verbose, self.test_discovery)
    
    def test_init(self):
        """Test TestExecutor initialization."""
        self.assertEqual(self.executor._python_path, self.python_path)
        self.assertEqual(self.executor._verbose, self.verbose)
        self.assertEqual(self.executor._test_discovery, self.test_discovery)
        self.assertIsNotNone(self.executor._parser)
    
    @patch('danielutils.tools.unittest_test_runner.core.execution.subprocess.run')
    def test_run_test_function_success(self, mock_run):
        """Test running a single test function successfully."""
        # Mock successful subprocess result
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "test_function1 (tests.test_module.TestClass) ... ok\n\nRan 1 test in 0.001s\n\nOK"
        mock_result.stderr = ""
        mock_run.return_value = mock_result
        
        # Mock parser to return test function state
        with patch.object(self.executor._parser, 'parse_test_output') as mock_parse:
            mock_parse.return_value = (
                [TestFunctionState(
                    function_name="test_function1",
                    status="passed",
                    runtime=0.001,
                    timestamp="2024-01-01 12:00:00",
                    error_message="",
                    warning_count=0,
                    should_skip=False,
                    skip_reason=""
                )],
                "OK",
                0.001
            )
            
            result = self.executor.run_test_function(
                "tests.test_module", 
                "TestClass", 
                "test_function1", 
                0, 
                1
            )
        
        self.assertIsInstance(result, TestFunctionState)
        self.assertEqual(result.function_name, "test_function1")
        self.assertEqual(result.status, "passed")
        
        # Verify subprocess was called correctly
        expected_cmd = [
            self.python_path, "-m", "unittest", 
            "tests.test_module.TestClass.test_function1", "-v"
        ]
        mock_run.assert_called_once_with(
            expected_cmd, capture_output=True, text=True, timeout=60
        )
    
    @patch('danielutils.tools.unittest_test_runner.core.execution.subprocess.run')
    def test_run_test_function_failure(self, mock_run):
        """Test running a single test function that fails."""
        # Mock failed subprocess result
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stdout = "test_function1 (tests.test_module.TestClass) ... FAIL\n\nRan 1 test in 0.001s\n\nFAILED (failures=1)"
        mock_result.stderr = ""
        mock_run.return_value = mock_result
        
        # Mock parser to return failed test function state
        with patch.object(self.executor._parser, 'parse_test_output') as mock_parse:
            mock_parse.return_value = (
                [TestFunctionState(
                    function_name="test_function1",
                    status="failed",
                    runtime=0.001,
                    timestamp="2024-01-01 12:00:00",
                    error_message="AssertionError: Test failed",
                    warning_count=0,
                    should_skip=False,
                    skip_reason=""
                )],
                "FAILED (failures=1)",
                0.001
            )
            
            result = self.executor.run_test_function(
                "tests.test_module", 
                "TestClass", 
                "test_function1", 
                0, 
                1
            )
        
        self.assertIsInstance(result, TestFunctionState)
        self.assertEqual(result.function_name, "test_function1")
        self.assertEqual(result.status, "failed")
        self.assertEqual(result.error_message, "AssertionError: Test failed")
    
    @patch('danielutils.tools.unittest_test_runner.core.execution.subprocess.run')
    def test_run_test_function_exception(self, mock_run):
        """Test running a test function that raises an exception."""
        # Mock subprocess raising an exception
        mock_run.side_effect = subprocess.TimeoutExpired("python", 300)
        
        result = self.executor.run_test_function(
            "tests.test_module", 
            "TestClass", 
            "test_function1", 
            0, 
            1
        )
        
        self.assertIsInstance(result, TestFunctionState)
        self.assertEqual(result.function_name, "test_function1")
        self.assertEqual(result.status, "error")
        self.assertIn("Error running test", result.error_message)
    
    def test_run_test_class_with_discovery(self):
        """Test running a test class using discovery information."""
        with patch.object(self.executor, 'run_test_function') as mock_run_function:
            # Mock individual function results
            mock_run_function.side_effect = [
                TestFunctionState(
                    function_name="test_function1",
                    status="passed",
                    runtime=0.001,
                    timestamp="2024-01-01 12:00:00",
                    error_message="",
                    warning_count=0,
                    should_skip=False,
                    skip_reason=""
                ),
                TestFunctionState(
                    function_name="test_function2",
                    status="failed",
                    runtime=0.002,
                    timestamp="2024-01-01 12:00:01",
                    error_message="AssertionError",
                    warning_count=0,
                    should_skip=False,
                    skip_reason=""
                )
            ]
            
            results = self.executor.run_test_class(
                "tests.test_module", 
                "TestClass", 
                0, 
                1
            )
        
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].function_name, "test_function1")
        self.assertEqual(results[0].status, "passed")
        self.assertEqual(results[1].function_name, "test_function2")
        self.assertEqual(results[1].status, "failed")
        
        # Verify run_test_function was called for each function
        expected_calls = [
            call("tests.test_module", "TestClass", "test_function1", 0, 2),
            call("tests.test_module", "TestClass", "test_function2", 1, 2)
        ]
        mock_run_function.assert_has_calls(expected_calls)
    
    @patch('danielutils.tools.unittest_test_runner.core.execution.subprocess.run')
    def test_run_test_class_fallback(self, mock_run):
        """Test running a test class using fallback method when no discovery info."""
        # Create executor without discovery info
        executor = TestExecutor(self.python_path, self.verbose, None)
        
        # Mock successful subprocess result
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "test_function1 (tests.test_module.TestClass) ... ok\ntest_function2 (tests.test_module.TestClass) ... ok\n\nRan 2 tests in 0.001s\n\nOK"
        mock_result.stderr = ""
        mock_run.return_value = mock_result
        
        # Mock parser to return test function states
        with patch.object(executor._parser, 'parse_test_output') as mock_parse:
            mock_parse.return_value = (
                [
                    TestFunctionState(
                        function_name="test_function1",
                        status="passed",
                        runtime=0.001,
                        timestamp="2024-01-01 12:00:00",
                        error_message="",
                        warning_count=0,
                        should_skip=False,
                        skip_reason=""
                    ),
                    TestFunctionState(
                        function_name="test_function2",
                        status="passed",
                        runtime=0.001,
                        timestamp="2024-01-01 12:00:00",
                        error_message="",
                        warning_count=0,
                        should_skip=False,
                        skip_reason=""
                    )
                ],
                "OK",
                0.001
            )
            
            results = executor.run_test_class(
                "tests.test_module", 
                "TestClass", 
                0, 
                1
            )
        
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].function_name, "test_function1")
        self.assertEqual(results[1].function_name, "test_function2")
        
        # Verify subprocess was called with class target
        expected_cmd = [self.python_path, "-m", "unittest", "tests.test_module.TestClass", "-v"]
        mock_run.assert_called_once_with(
            expected_cmd, capture_output=True, text=True, timeout=60
        )
    
    def test_run_test_file_with_discovery(self):
        """Test running a test file using discovery information."""
        with patch.object(self.executor, 'run_test_class') as mock_run_class:
            # Mock class results
            mock_run_class.return_value = [
                TestFunctionState(
                    function_name="test_function1",
                    status="passed",
                    runtime=0.001,
                    timestamp="2024-01-01 12:00:00",
                    error_message="",
                    warning_count=0,
                    should_skip=False,
                    skip_reason=""
                )
            ]
            
            results = self.executor.run_test_file(
                "tests.test_module", 
                0, 
                1
            )
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].function_name, "test_function1")
        
        # Verify run_test_class was called
        mock_run_class.assert_called_once_with("tests.test_module", "TestClass", 0, 1)
    
    @patch('danielutils.tools.unittest_test_runner.core.execution.subprocess.run')
    def test_run_test_file_fallback(self, mock_run):
        """Test running a test file using fallback method when no discovery info."""
        # Create executor without discovery info
        executor = TestExecutor(self.python_path, self.verbose, None)
        
        # Mock successful subprocess result
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "test_function1 (tests.test_module.TestClass) ... ok\n\nRan 1 test in 0.001s\n\nOK"
        mock_result.stderr = ""
        mock_run.return_value = mock_result
        
        # Mock parser to return test function state
        with patch.object(executor._parser, 'parse_test_output') as mock_parse:
            mock_parse.return_value = (
                [TestFunctionState(
                    function_name="test_function1",
                    status="passed",
                    runtime=0.001,
                    timestamp="2024-01-01 12:00:00",
                    error_message="",
                    warning_count=0,
                    should_skip=False,
                    skip_reason=""
                )],
                "OK",
                0.001
            )
            
            results = executor.run_test_file(
                "tests.test_module", 
                0, 
                1
            )
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].function_name, "test_function1")
        
        # Verify subprocess was called with module target
        expected_cmd = [self.python_path, "-m", "unittest", "tests.test_module", "-v"]
        mock_run.assert_called_once_with(
            expected_cmd, capture_output=True, text=True, timeout=60
        )


if __name__ == '__main__':
    unittest.main()
