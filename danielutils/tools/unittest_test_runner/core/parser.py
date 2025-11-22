"""
Output parsing and result processing functionality.
"""

import logging
import time
from typing import List, Tuple
from ..models import TestFunctionState

logger = logging.getLogger(__name__)


class TestOutputParser:
    """Handles parsing of unittest output and creating test states."""
    
    def __init__(self, verbose: str = "class"):
        logger.debug("Initializing TestOutputParser with verbose=%s", verbose)
        self._verbose = verbose
    
    def parse_test_output(self, output_lines: List[str], stderr_lines: List[str]) -> Tuple[List[TestFunctionState], List[str], List[str]]:
        """Parse unittest output to extract individual test function results."""
        logger.debug("Parsing test output: %d output lines, %d stderr lines", len(output_lines), len(stderr_lines))
        test_functions = []
        errors = []
        warnings = []
        
        # Collect errors and warnings from stderr
        for line in stderr_lines:
            if "Error" in line or "error" in line:
                errors.append(line.strip())
                logger.debug("Found error in stderr: %s", line.strip())
            elif "Warning" in line or "warning" in line:
                warnings.append(line.strip())
                logger.debug("Found warning in stderr: %s", line.strip())
        
        # Parse individual test results
        if self._verbose == "function":
            print(f"DEBUG: Processing {len(output_lines)} output lines")
            for i, line in enumerate(output_lines[:10]):  # Show first 10 lines
                print(f"DEBUG: Line {i}: {line}")
        
        # Combine output and stderr lines for processing (unittest can output to either)
        all_lines = output_lines + stderr_lines
        
        # Process lines in pairs - test name line followed by status line
        i = 0
        while i < len(all_lines):
            line = all_lines[i]
            
            # Look for test method lines like "test_something (class_name)"
            if "test_" in line and "(" in line and ")" in line:
                logger.debug("Found test name line: %s", line)
                if self._verbose == "function":
                    print(f"DEBUG: Found test name line: {line}")
                
                # Extract test name
                parts = line.split()
                test_name = None
                for part in parts:
                    if part.startswith("test_"):
                        test_name = part
                        break
                
                if test_name:
                    logger.debug("Extracted test name: %s", test_name)
                    # Check if status is on the same line
                    status = None
                    runtime = 0.0
                    
                    if "ok" in line:
                        status = "passed"
                        # Try to extract runtime from the same line if present
                        try:
                            import re
                            runtime_match = re.search(r'ok\s*\((\d+\.?\d*)\s*s?\)', line)
                            if runtime_match:
                                runtime = float(runtime_match.group(1))
                                logger.debug("Extracted runtime from same line: %.3fs", runtime)
                        except (ValueError, IndexError):
                            pass
                    elif "FAIL" in line:
                        status = "failed"
                    elif "ERROR" in line:
                        status = "error"
                    elif "SKIP" in line or "skip" in line:
                        status = "skipped"
                    else:
                        # Status is on the next line
                        if i + 1 < len(all_lines):
                            next_line = all_lines[i + 1]
                            logger.debug("Checking next line for status: %s", next_line)
                            if self._verbose == "function":
                                print(f"DEBUG: Checking next line for status: {next_line}")
                            
                            if "ok" in next_line:
                                status = "passed"
                            elif "FAIL" in next_line:
                                status = "failed"
                            elif "ERROR" in next_line:
                                status = "error"
                            elif "SKIP" in next_line or "skip" in next_line:
                                status = "skipped"
                            
                            # Try to extract runtime from the status line
                            try:
                                # Look for patterns like "0.001s" or "0.001"
                                import re
                                runtime_match = re.search(r'(\d+\.?\d*)\s*s?', next_line)
                                if runtime_match:
                                    runtime = float(runtime_match.group(1))
                                    logger.debug("Extracted runtime: %.3fs", runtime)
                            except (ValueError, IndexError):
                                logger.debug("Failed to extract runtime from: %s", next_line)
                                pass
                    
                    # Create test function state
                    test_function = TestFunctionState(
                        function_name=test_name,
                        status=status or "unknown",
                        runtime=runtime,
                        timestamp=time.strftime('%Y-%m-%d %H:%M:%S'),
                        error_message="",
                        warning_count=0,
                        should_skip=False,
                        skip_reason=""
                    )
                    test_functions.append(test_function)
                    logger.debug("Added test function: %s - %s (%.3fs)", test_name, status, runtime)
                    
                    if self._verbose == "function":
                        print(f"DEBUG: Added test function: {test_name} - {status} ({runtime}s)")
            
            i += 1
        
        # If no individual tests were found, try to parse from summary
        if not test_functions:
            logger.warning("No individual test functions found, looking for summary")
            # Look for summary lines like "Ran X tests in Y.YYs"
            for line in all_lines:
                if "Ran" in line and "tests" in line:
                    logger.debug("Found summary line: %s", line)
                    # Only create a placeholder if there were actually tests run
                    # Check if the summary indicates 0 tests
                    import re
                    match = re.search(r'Ran (\d+) tests', line)
                    if match and int(match.group(1)) > 0:
                        # This is a summary line, but we can't extract individual results
                        # Just create a placeholder
                        test_function = TestFunctionState(
                            function_name="unknown",
                            status="unknown",
                            runtime=0.0,
                            timestamp=time.strftime('%Y-%m-%d %H:%M:%S'),
                            error_message="No individual test results found",
                            warning_count=0,
                            should_skip=False,
                            skip_reason=""
                        )
                        test_functions.append(test_function)
                    break
        
        logger.info("Parsed %d test functions, %d errors, %d warnings", len(test_functions), len(errors), len(warnings))
        return test_functions, errors, warnings
