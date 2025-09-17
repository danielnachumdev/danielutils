"""
Tests for the CLI interface.
"""
import unittest
from unittest.mock import patch, MagicMock
import sys
from io import StringIO

from danielutils.tools.unittest_test_runner.cli import run_tests
from tests.test_tools.base import BaseToolTest


class TestCLI(BaseToolTest):
    """Test cases for CLI interface."""
    
    def setUp(self):
        """Set up test fixtures."""
        super().setUp()
        self.original_argv = sys.argv
        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr
    
    def tearDown(self):
        """Clean up test fixtures."""
        sys.argv = self.original_argv
        sys.stdout = self.original_stdout
        sys.stderr = self.original_stderr
        super().tearDown()
    
    @patch('danielutils.tools.unittest_test_runner.cli.TestRunner')
    def test_run_tests_default_parameters(self, mock_runner_class):
        """Test run_tests with default parameters."""
        # Mock TestRunner instance
        mock_runner = MagicMock()
        mock_runner.run_tests.return_value = MagicMock()
        mock_runner_class.return_value = mock_runner
        
        # Call run_tests with default parameters
        result = run_tests()
        
        # Verify TestRunner was instantiated with correct parameters
        mock_runner_class.assert_called_once_with(
            python_path=None,  # Will use sys.executable
            results_file="test_results.json",
            skip_threshold_hours=24,
            force_run=False,
            test_name=None,
            target=None,
            verbose="class",
            show_function_results=False
        )
        
        # Verify run_all_tests was called
        mock_runner.run_all_tests.assert_called_once()
    
    @patch('danielutils.tools.unittest_test_runner.cli.TestRunner')
    def test_run_tests_with_verbose_function(self, mock_runner_class):
        """Test run_tests with verbose set to function."""
        # Mock TestRunner instance
        mock_runner = MagicMock()
        mock_runner.run_tests.return_value = MagicMock()
        mock_runner_class.return_value = mock_runner
        
        # Call run_tests with verbose="function"
        result = run_tests(verbose="function")
        
        # Verify TestRunner was instantiated with correct parameters
        mock_runner_class.assert_called_once_with(
            python_path=None,
            results_file="test_results.json",
            skip_threshold_hours=24,
            force_run=False,
            test_name=None,
            target=None,
            verbose="function",
            show_function_results=False
        )
    
    @patch('danielutils.tools.unittest_test_runner.cli.TestRunner')
    def test_run_tests_with_target(self, mock_runner_class):
        """Test run_tests with target specified."""
        # Mock TestRunner instance
        mock_runner = MagicMock()
        mock_runner.run_tests.return_value = MagicMock()
        mock_runner_class.return_value = mock_runner
        
        # Call run_tests with target
        target = "tests.test_module.TestClass.test_function"
        result = run_tests(target=target)
        
        # Verify TestRunner was instantiated with correct parameters
        mock_runner_class.assert_called_once_with(
            python_path=None,
            results_file="test_results.json",
            skip_threshold_hours=24,
            force_run=False,
            test_name=None,
            target=target,
            verbose="class",
            show_function_results=False
        )
    
    @patch('danielutils.tools.unittest_test_runner.cli.TestRunner')
    def test_run_tests_with_custom_results_file(self, mock_runner_class):
        """Test run_tests with custom results file."""
        # Mock TestRunner instance
        mock_runner = MagicMock()
        mock_runner.run_tests.return_value = MagicMock()
        mock_runner_class.return_value = mock_runner
        
        # Call run_tests with custom results file
        results_file = "custom_results.json"
        result = run_tests(results_file=results_file)
        
        # Verify TestRunner was instantiated with correct parameters
        mock_runner_class.assert_called_once_with(
            python_path=None,
            results_file=results_file,
            skip_threshold_hours=24,
            force_run=False,
            test_name=None,
            target=None,
            verbose="class",
            show_function_results=False
        )
    
    @patch('danielutils.tools.unittest_test_runner.cli.TestRunner')
    def test_run_tests_with_python_path(self, mock_runner_class):
        """Test run_tests with custom python path."""
        # Mock TestRunner instance
        mock_runner = MagicMock()
        mock_runner.run_tests.return_value = MagicMock()
        mock_runner_class.return_value = mock_runner
        
        # Call run_tests with custom python path
        python_path = "/usr/bin/python3"
        result = run_tests(python_path=python_path)
        
        # Verify TestRunner was instantiated with correct parameters
        mock_runner_class.assert_called_once_with(
            python_path=python_path,
            results_file="test_results.json",
            skip_threshold_hours=24,
            force_run=False,
            test_name=None,
            target=None,
            verbose="class",
            show_function_results=False
        )
    
    @patch('danielutils.tools.unittest_test_runner.cli.TestRunner')
    def test_run_tests_all_parameters(self, mock_runner_class):
        """Test run_tests with all parameters specified."""
        # Mock TestRunner instance
        mock_runner = MagicMock()
        mock_runner.run_tests.return_value = MagicMock()
        mock_runner_class.return_value = mock_runner
        
        # Call run_tests with all parameters
        result = run_tests(
            python_path="/usr/bin/python3",
            verbose="function",
            results_file="custom_results.json",
            target="tests.test_module.TestClass.test_function"
        )
        
        # Verify TestRunner was instantiated with correct parameters
        mock_runner_class.assert_called_once_with(
            python_path="/usr/bin/python3",
            results_file="custom_results.json",
            skip_threshold_hours=24,
            force_run=False,
            test_name=None,
            target="tests.test_module.TestClass.test_function",
            verbose="function",
            show_function_results=False
        )
    
    @patch('danielutils.tools.unittest_test_runner.cli.TestRunner')
    def test_run_tests_returns_summary(self, mock_runner_class):
        """Test that run_tests returns the summary from TestRunner."""
        # Mock TestRunner instance and summary
        mock_summary = MagicMock()
        mock_runner = MagicMock()
        mock_runner.run_tests.return_value = mock_summary
        mock_runner_class.return_value = mock_runner
        
        # Call run_tests
        result = run_tests()
        
        # Verify the summary is returned (run_all_tests returns None)
        self.assertIsNone(result)
    
    def test_run_tests_verbose_levels(self):
        """Test that all valid verbose levels are accepted."""
        valid_levels = ["module", "file", "class", "function"]
        
        for level in valid_levels:
            with self.subTest(verbose=level):
                with patch('danielutils.tools.unittest_test_runner.cli.TestRunner') as mock_runner_class:
                    mock_runner = MagicMock()
                    mock_runner.run_tests.return_value = MagicMock()
                    mock_runner_class.return_value = mock_runner
                    
                    # This should not raise an exception
                    result = run_tests(verbose=level)
                    
                    # Verify TestRunner was called with correct verbose level
                    mock_runner_class.assert_called_once_with(
                        python_path=None,
                        results_file="test_results.json",
                        skip_threshold_hours=24,
                        force_run=False,
                        test_name=None,
                        target=None,
                        verbose=level,
                        show_function_results=False
                    )


if __name__ == '__main__':
    unittest.main()
