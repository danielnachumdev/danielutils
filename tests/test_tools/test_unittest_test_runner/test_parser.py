"""
Tests for the TestOutputParser class.
"""
import unittest
from unittest.mock import patch

from danielutils.tools.unittest_test_runner.core.parser import TestOutputParser
from danielutils.tools.unittest_test_runner.models import TestFunctionState
from tests.test_tools.base import BaseToolTest


class TestTestOutputParser(BaseToolTest):
    """Test cases for TestOutputParser."""
    
    def setUp(self):
        """Set up test fixtures."""
        super().setUp()
        self.verbose = "class"
        self.parser = TestOutputParser(self.verbose)
    
    def test_init(self):
        """Test TestOutputParser initialization."""
        self.assertEqual(self.parser._verbose, self.verbose)
    
    def test_parse_test_output_success(self):
        """Test parsing successful test output."""
        output_lines = [
            "test_function_name (module.TestClass) ... ok",
            "test_another_function (module.TestClass) ... ok",
            "",
            "Ran 2 tests in 0.001s",
            "",
            "OK"
        ]
        stderr_lines = []
        
        test_functions, errors, warnings = self.parser.parse_test_output(output_lines, stderr_lines)
        
        self.assertEqual(len(test_functions), 2)
        self.assertEqual(test_functions[0].function_name, "test_function_name")
        self.assertEqual(test_functions[0].status, "passed")
        self.assertEqual(test_functions[1].function_name, "test_another_function")
        self.assertEqual(test_functions[1].status, "passed")
        self.assertEqual(len(errors), 0)
        self.assertEqual(len(warnings), 0)
    
    def test_parse_test_output_failure(self):
        """Test parsing failed test output."""
        output_lines = [
            "test_function_name (module.TestClass) ... FAIL",
            "test_another_function (module.TestClass) ... ok",
            "",
            "Ran 2 tests in 0.001s",
            "",
            "FAILED (failures=1)"
        ]
        stderr_lines = []
        
        test_functions, errors, warnings = self.parser.parse_test_output(output_lines, stderr_lines)
        
        self.assertEqual(len(test_functions), 2)
        self.assertEqual(test_functions[0].function_name, "test_function_name")
        self.assertEqual(test_functions[0].status, "failed")
        self.assertEqual(test_functions[1].function_name, "test_another_function")
        self.assertEqual(test_functions[1].status, "passed")
        self.assertEqual(len(errors), 0)
        self.assertEqual(len(warnings), 0)
    
    def test_parse_test_output_error(self):
        """Test parsing error test output."""
        output_lines = [
            "test_function_name (module.TestClass) ... ERROR",
            "test_another_function (module.TestClass) ... ok",
            "",
            "Ran 2 tests in 0.001s",
            "",
            "FAILED (errors=1)"
        ]
        stderr_lines = []
        
        test_functions, errors, warnings = self.parser.parse_test_output(output_lines, stderr_lines)
        
        self.assertEqual(len(test_functions), 2)
        self.assertEqual(test_functions[0].function_name, "test_function_name")
        self.assertEqual(test_functions[0].status, "error")
        self.assertEqual(test_functions[1].function_name, "test_another_function")
        self.assertEqual(test_functions[1].status, "passed")
        self.assertEqual(len(errors), 0)
        self.assertEqual(len(warnings), 0)
    
    def test_parse_test_output_skipped(self):
        """Test parsing skipped test output."""
        output_lines = [
            "test_function_name (module.TestClass) ... skipped 'reason'",
            "test_another_function (module.TestClass) ... ok",
            "",
            "Ran 2 tests in 0.001s",
            "",
            "OK (skipped=1)"
        ]
        stderr_lines = []
        
        test_functions, errors, warnings = self.parser.parse_test_output(output_lines, stderr_lines)
        
        self.assertEqual(len(test_functions), 2)
        self.assertEqual(test_functions[0].function_name, "test_function_name")
        self.assertEqual(test_functions[0].status, "skipped")
        self.assertEqual(test_functions[1].function_name, "test_another_function")
        self.assertEqual(test_functions[1].status, "passed")
        self.assertEqual(len(errors), 0)
        self.assertEqual(len(warnings), 0)
    
    def test_parse_test_output_mixed_status(self):
        """Test parsing mixed status test output."""
        output_lines = [
            "test_passed (module.TestClass) ... ok",
            "test_failed (module.TestClass) ... FAIL",
            "test_error (module.TestClass) ... ERROR",
            "test_skipped (module.TestClass) ... skipped 'reason'",
            "",
            "Ran 4 tests in 0.001s",
            "",
            "FAILED (failures=1, errors=1, skipped=1)"
        ]
        stderr_lines = []
        
        test_functions, errors, warnings = self.parser.parse_test_output(output_lines, stderr_lines)
        
        self.assertEqual(len(test_functions), 4)
        statuses = [tf.status for tf in test_functions]
        self.assertIn("passed", statuses)
        self.assertIn("failed", statuses)
        self.assertIn("error", statuses)
        self.assertIn("skipped", statuses)
        self.assertEqual(len(errors), 0)
        self.assertEqual(len(warnings), 0)
    
    def test_parse_test_output_with_stderr(self):
        """Test parsing test output when tests write to stderr."""
        output_lines = []
        stderr_lines = [
            "test_function_name (module.TestClass) ... ok",
            "test_another_function (module.TestClass) ... FAIL",
            "",
            "Ran 2 tests in 0.001s",
            "",
            "FAILED (failures=1)"
        ]
        
        test_functions, errors, warnings = self.parser.parse_test_output(output_lines, stderr_lines)
        
        self.assertEqual(len(test_functions), 2)
        self.assertEqual(test_functions[0].function_name, "test_function_name")
        self.assertEqual(test_functions[0].status, "passed")
        self.assertEqual(test_functions[1].function_name, "test_another_function")
        self.assertEqual(test_functions[1].status, "failed")
        self.assertEqual(len(errors), 0)
        self.assertEqual(len(warnings), 0)
    
    def test_parse_test_output_empty(self):
        """Test parsing empty test output."""
        output_lines = []
        stderr_lines = []
        
        test_functions, errors, warnings = self.parser.parse_test_output(output_lines, stderr_lines)
        
        self.assertEqual(len(test_functions), 0)
        self.assertEqual(len(errors), 0)
        self.assertEqual(len(warnings), 0)
    
    def test_parse_test_output_malformed(self):
        """Test parsing malformed test output."""
        output_lines = [
            "not a test line",
            "another non-test line",
            "",
            "Ran 0 tests in 0.000s",
            "",
            "OK"
        ]
        stderr_lines = []
        
        test_functions, errors, warnings = self.parser.parse_test_output(output_lines, stderr_lines)
        
        self.assertEqual(len(test_functions), 0)
        self.assertEqual(len(errors), 0)
        self.assertEqual(len(warnings), 0)
    
    def test_parse_test_output_with_runtime(self):
        """Test parsing test output with runtime information."""
        output_lines = [
            "test_function_name (module.TestClass) ... ok (0.123s)",
            "test_another_function (module.TestClass) ... ok (0.456s)",
            "",
            "Ran 2 tests in 0.579s",
            "",
            "OK"
        ]
        stderr_lines = []
        
        test_functions, errors, warnings = self.parser.parse_test_output(output_lines, stderr_lines)
        
        self.assertEqual(len(test_functions), 2)
        # Verify that runtime parsing works for individual tests
        self.assertEqual(test_functions[0].runtime, 0.123)
        self.assertEqual(test_functions[1].runtime, 0.456)
        self.assertEqual(len(errors), 0)
        self.assertEqual(len(warnings), 0)


if __name__ == '__main__':
    unittest.main()
