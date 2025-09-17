"""
Test execution hierarchy functionality.
Handles the core execution context with _run_test_function as the base.
"""

import logging
import time
import subprocess
from typing import List, Optional, Literal
from ..models import TestFunctionState, TestResult, ModuleState
from .parser import TestOutputParser

logger = logging.getLogger(__name__)

VerboseLevel = Literal["module", "file", "class", "function"]


class TestExecutor:
    """Handles hierarchical test execution with _run_test_function as the core."""
    
    def __init__(self, python_path: str, verbose: VerboseLevel = "class", 
                 test_discovery: Optional[object] = None):
        logger.debug("Initializing TestExecutor with python_path=%s, verbose=%s", python_path, verbose)
        self._python_path = python_path
        self._verbose = verbose
        self._test_discovery = test_discovery
        self._parser = TestOutputParser(verbose)
    
    def run_test_function(self, module_path: str, test_class: str, test_function: str, 
                         function_index: int = 0, total_functions: int = 0) -> TestFunctionState:
        """Run a single test function and return its state. This is the core execution context."""
        logger.debug("Running test function: %s.%s.%s", module_path, test_class, test_function)
        indent = "        "  # 8 spaces for function level
        
        if self._verbose == "function":
            progress = f"[{function_index + 1}/{total_functions}]" if total_functions > 0 else ""
            print(f"{indent}{progress} Running test function: {test_class}.{test_function}")
        
        try:
            # Run specific test function: python -m unittest module.class.function
            cmd = [self._python_path, "-m", "unittest", f"{module_path}.{test_class}.{test_function}", "-v"]
            logger.debug("Executing command: %s", " ".join(cmd))
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            # Parse the output
            output_lines = result.stdout.split('\n')
            stderr_lines = result.stderr.split('\n')
            
            # If stdout is empty but stderr has test output, use stderr
            if not any("test_" in line for line in output_lines) and any("test_" in line for line in stderr_lines):
                logger.debug("Using stderr output for test function: %s", test_function)
                output_lines = stderr_lines
                stderr_lines = []
            
            # Parse test function result
            test_functions, _, _ = self._parser.parse_test_output(output_lines, stderr_lines)
            
            if test_functions:
                test_state = test_functions[0]
                logger.debug("Test function %s completed with status: %s (runtime: %.3fs)", 
                           test_function, test_state.status, test_state.runtime)
                if self._verbose == "function":
                    status_symbol = "✓" if test_state.status == "passed" else "✗" if test_state.status == "failed" else "⚠" if test_state.status == "error" else "⏭" if test_state.status == "skipped" else "?"
                    print(f"{indent}  {status_symbol} {test_function} ({test_state.status}) - {test_state.runtime:.3f}s")
                return test_state
            else:
                # Create a failed state if parsing failed
                logger.warning("Failed to parse test output for function: %s", test_function)
                error_state = TestFunctionState(
                    function_name=test_function,
                    status="error",
                    runtime=0.0,
                    timestamp=time.strftime('%Y-%m-%d %H:%M:%S'),
                    error_message="Failed to parse test output",
                    warning_count=0,
                    should_skip=False,
                    skip_reason=""
                )
                if self._verbose == "function":
                    print(f"{indent}  ⚠ {test_function} (error) - Failed to parse output")
                return error_state
                
        except Exception as e:
            logger.error("Error running test function %s: %s", test_function, e)
            error_state = TestFunctionState(
                function_name=test_function,
                status="error",
                runtime=0.0,
                timestamp=time.strftime('%Y-%m-%d %H:%M:%S'),
                error_message=f"Error running test: {e}",
                warning_count=0,
                should_skip=False,
                skip_reason=""
            )
            if self._verbose == "function":
                print(f"{indent}  ⚠ {test_function} (error) - {e}")
            return error_state
    
    def run_test_class(self, module_path: str, test_class: str, class_index: int = 0, total_classes: int = 0) -> List[TestFunctionState]:
        """Run all test functions in a test class and return their states."""
        logger.debug("Running test class: %s.%s", module_path, test_class)
        indent = "      "  # 6 spaces for class level
        
        if self._verbose in ["class", "function"]:
            progress = f"[{class_index + 1}/{total_classes}]" if total_classes > 0 else ""
            print(f"{indent}{progress} Running test class: {test_class}")
        
        # Get functions for this class from discovery
        class_key = f"{module_path}.{test_class}"
        class_functions = self._test_discovery.functions.get(class_key, []) if self._test_discovery else []
        logger.debug("Found %d functions in class %s", len(class_functions), test_class)
        
        if not class_functions:
            # Fallback: run the class as a whole
            logger.debug("No discovery info for class %s, running as whole", test_class)
            try:
                cmd = [self._python_path, "-m", "unittest", f"{module_path}.{test_class}", "-v"]
                logger.debug("Executing class command: %s", " ".join(cmd))
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
                
                output_lines = result.stdout.split('\n')
                stderr_lines = result.stderr.split('\n')
                
                if not any("test_" in line for line in output_lines) and any("test_" in line for line in stderr_lines):
                    logger.debug("Using stderr output for class: %s", test_class)
                    output_lines = stderr_lines
                    stderr_lines = []
                
                test_functions, _, _ = self._parser.parse_test_output(output_lines, stderr_lines)
                logger.debug("Class %s completed with %d test functions", test_class, len(test_functions))
                
                if self._verbose == "function" and test_functions:
                    for test_func in test_functions:
                        status_symbol = "✓" if test_func.status == "passed" else "✗" if test_func.status == "failed" else "⚠" if test_func.status == "error" else "⏭" if test_func.status == "skipped" else "?"
                        print(f"        {status_symbol} {test_func.function_name} ({test_func.status}) - {test_func.runtime:.3f}s")
                
                return test_functions
                    
            except Exception as e:
                logger.error("Failed to run test class %s: %s", test_class, e)
                if self._verbose in ["class", "function"]:
                    print(f"        ERROR: Failed to run test class {test_class}: {e}")
                return []
        else:
            # Run each function individually using run_test_function
            logger.debug("Running %d individual functions in class %s", len(class_functions), test_class)
            test_functions = []
            for i, function_name in enumerate(class_functions):
                test_state = self.run_test_function(module_path, test_class, function_name, i, len(class_functions))
                test_functions.append(test_state)
            
            # Show class summary
            passed = sum(1 for t in test_functions if t.status == "passed")
            failed = sum(1 for t in test_functions if t.status == "failed")
            errors = sum(1 for t in test_functions if t.status == "error")
            skipped = sum(1 for t in test_functions if t.status == "skipped")
            logger.debug("Class %s summary: %d passed, %d failed, %d errors, %d skipped", 
                        test_class, passed, failed, errors, skipped)
            
            if self._verbose in ["class", "function"]:
                print(f"{indent}  {test_class}: {passed} passed, {failed} failed, {errors} errors, {skipped} skipped")
            
            return test_functions
    
    def run_test_file(self, module_path: str, file_index: int = 0, total_files: int = 0) -> List[TestFunctionState]:
        """Run all test classes in a test file and return all test function states."""
        logger.debug("Running test file: %s", module_path)
        indent = "    "  # 4 spaces for file level
        
        if self._verbose in ["file", "class", "function"]:
            progress = f"[{file_index + 1}/{total_files}]" if total_files > 0 else ""
            print(f"{indent}{progress} Running test file: {module_path}")
        
        # Get classes for this module from discovery
        module_classes = self._test_discovery.classes.get(module_path, []) if self._test_discovery else []
        logger.debug("Found %d classes in module %s", len(module_classes), module_path)
        
        if not module_classes:
            # Fallback: run the module as a whole
            logger.debug("No discovery info for module %s, running as whole", module_path)
            try:
                cmd = [self._python_path, "-m", "unittest", module_path, "-v"]
                logger.debug("Executing module command: %s", " ".join(cmd))
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
                
                output_lines = result.stdout.split('\n')
                stderr_lines = result.stderr.split('\n')
                
                if not any("test_" in line for line in output_lines) and any("test_" in line for line in stderr_lines):
                    logger.debug("Using stderr output for module: %s", module_path)
                    output_lines = stderr_lines
                    stderr_lines = []
                
                test_functions, _, _ = self._parser.parse_test_output(output_lines, stderr_lines)
                logger.debug("Module %s completed with %d test functions", module_path, len(test_functions))
                
                if self._verbose in ["class", "function"] and test_functions:
                    # Group by test class
                    classes = {}
                    for test_func in test_functions:
                        class_name = "UnknownClass"  # We'll improve this later
                        if class_name not in classes:
                            classes[class_name] = []
                        classes[class_name].append(test_func)
                    
                    for class_name, class_tests in classes.items():
                        if self._verbose == "class":
                            passed = sum(1 for t in class_tests if t.status == "passed")
                            failed = sum(1 for t in class_tests if t.status == "failed")
                            errors = sum(1 for t in class_tests if t.status == "error")
                            print(f"      {class_name}: {passed} passed, {failed} failed, {errors} errors")
                        elif self._verbose == "function":
                            print(f"      {class_name}:")
                            for test_func in class_tests:
                                status_symbol = "✓" if test_func.status == "passed" else "✗" if test_func.status == "failed" else "⚠" if test_func.status == "error" else "⏭" if test_func.status == "skipped" else "?"
                                print(f"        {status_symbol} {test_func.function_name} ({test_func.status}) - {test_func.runtime:.3f}s")
                
                return test_functions
                    
            except Exception as e:
                logger.error("Failed to run test file %s: %s", module_path, e)
                if self._verbose in ["file", "class", "function"]:
                    print(f"        ERROR: Failed to run test file {module_path}: {e}")
                return []
        else:
            # Run each class individually using run_test_class
            logger.debug("Running %d individual classes in module %s", len(module_classes), module_path)
            all_test_functions = []
            for i, class_name in enumerate(module_classes):
                class_functions = self.run_test_class(module_path, class_name, i, len(module_classes))
                all_test_functions.extend(class_functions)
            
            # Show file summary
            passed = sum(1 for t in all_test_functions if t.status == "passed")
            failed = sum(1 for t in all_test_functions if t.status == "failed")
            errors = sum(1 for t in all_test_functions if t.status == "error")
            skipped = sum(1 for t in all_test_functions if t.status == "skipped")
            logger.debug("Module %s summary: %d passed, %d failed, %d errors, %d skipped", 
                        module_path, passed, failed, errors, skipped)
            
            if self._verbose in ["file", "class", "function"]:
                print(f"{indent}  {module_path}: {passed} passed, {failed} failed, {errors} errors, {skipped} skipped")
            
            return all_test_functions
