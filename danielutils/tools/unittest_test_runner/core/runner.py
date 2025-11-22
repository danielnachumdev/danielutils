"""
Main TestRunner orchestration functionality.
"""

import logging
import os
import sys
import time
import json
import subprocess
from typing import List, Optional, Literal
from ..models import TestFunctionState, ModuleState, TestResult, TestRunSummary, TestDiscovery
from .discovery import TestDiscoveryService
from .execution import TestExecutor
from .parser import TestOutputParser

logger = logging.getLogger(__name__)

VerboseLevel = Literal["module", "file", "class", "function"]


class TestRunner:
    """Smart test runner that executes tests module by module and collects detailed statistics."""
    
    def __init__(self, 
                 python_path: Optional[str] = None, 
                 results_file: str = "test_results.json", 
                 skip_threshold_hours: int = 24,
                 force_run: bool = False,
                 test_name: Optional[str] = None,
                 target: Optional[str] = None,
                 verbose: VerboseLevel = "class",
                 show_function_results: bool = False):
        logger.info("Initializing TestRunner with python_path=%s, results_file=%s, skip_threshold_hours=%d, force_run=%s, target=%s, verbose=%s", 
                   python_path, results_file, skip_threshold_hours, force_run, target, verbose)
        
        self.python_path = python_path or sys.executable
        self.results_file = results_file
        self.skip_threshold_hours = skip_threshold_hours
        self.force_run = force_run
        self.test_name = test_name
        self.target = target
        self.verbose = verbose
        self.show_function_results = show_function_results
        
        # Ensure we have a valid Python executable
        if not self.python_path or not os.path.exists(self.python_path):
            logger.warning("Invalid Python path provided, using sys.executable: %s", sys.executable)
            self.python_path = sys.executable
        
        # Validate verbose level (this should be caught by type checker, but good to have runtime check)
        valid_levels: List[VerboseLevel] = ["module", "file", "class", "function"]
        if self.verbose not in valid_levels:
            logger.error("Invalid verbose level '%s'. Must be one of: %s", self.verbose, valid_levels)
            raise ValueError(f"Invalid verbose level '{self.verbose}'. Must be one of: {valid_levels}")
        
        # Debug output (only in function level)
        if self.verbose == "function":
            logger.debug("Using Python executable: %s", self.python_path)
            print(f"DEBUG: Using Python executable: {self.python_path}")
        
        # Initialize services
        logger.debug("Initializing discovery service and parser")
        self.discovery_service = TestDiscoveryService(self.python_path, self.verbose)
        self.parser = TestOutputParser(self.verbose)
        
        # Initialize state
        self.results: List[TestResult] = []
        self.previous_results: Optional[TestRunSummary] = None
        logger.debug("Loading previous results from: %s", self.results_file)
        self._load_previous_results()
        
        # Discover test modules based on target
        logger.info("Starting test discovery phase")
        if self.verbose in ["module", "file", "class", "function"]:
            print("🔍 Test Discovery Phase")
            print("=" * 50)
        
        if self.target:
            # If target is specified, discover modules relative to target
            logger.info("Target specified, discovering modules for target: %s", self.target)
            if self.verbose in ["module", "file", "class", "function"]:
                print(f"🎯 Target specified: {self.target}")
            self.test_modules = self.discovery_service.discover_test_modules(target=self.target)
        else:
            # No target, discover all modules in default tests directory
            logger.info("No target specified, discovering all test modules")
            if self.verbose in ["module", "file", "class", "function"]:
                print("📁 No target specified, discovering all test modules")
            self.test_modules = self.discovery_service.discover_test_modules()
        
        logger.info("Discovered %d test modules", len(self.test_modules))
        self.test_discovery: Optional[TestDiscovery] = None
        self._discover_test_structure()
        
        # Apply target filtering if specified
        if self.target and self.test_discovery:
            logger.debug("Applying target filtering for: %s", self.target)
            target_module, target_class, target_function = self.discovery_service.parse_target(self.target)
            if target_module:
                self.test_discovery = self.discovery_service.create_focused_discovery(
                    target_module, target_class, target_function, self.test_discovery
                )
                logger.debug("Focused discovery created for target: %s (module: %s, class: %s, function: %s)", 
                           self.target, target_module, target_class, target_function)
                if self.verbose == "function":
                    print(f"DEBUG: Focused discovery created for target: {self.target}")
                    print(f"DEBUG: Target components - module: {target_module}, class: {target_class}, function: {target_function}")
        
        # Initialize executor
        logger.debug("Initializing test executor")
        self.executor = TestExecutor(self.python_path, self.verbose, self.test_discovery)
    
    def _discover_test_structure(self):
        """Discover the complete test structure for progress tracking."""
        logger.debug("Discovering test structure for %d modules", len(self.test_modules))
        self.test_discovery = self.discovery_service.discover_test_structure(self.test_modules)
        if self.test_discovery:
            logger.info("Test structure discovery complete: %d modules, %d classes, %d functions", 
                       self.test_discovery.total_modules, self.test_discovery.total_classes, self.test_discovery.total_functions)
    
    def _load_previous_results(self):
        """Load previous test results from JSON file."""
        if not os.path.exists(self.results_file):
            logger.info("No previous results file found: %s", self.results_file)
            print(f"No previous results file found: {self.results_file}")
            return
        
        try:
            logger.debug("Loading previous results from: %s", self.results_file)
            with open(self.results_file, 'r') as f:
                data = json.load(f)
                
                # Convert results list from dicts to TestResult objects
                if 'results' in data and isinstance(data['results'], list):
                    results = []
                    logger.debug("Converting %d previous results from dicts to objects", len(data['results']))
                    for result_dict in data['results']:
                        # Convert nested dicts to proper objects
                        if 'module_state' in result_dict:
                            module_state_dict = result_dict['module_state']
                            # Convert test_functions dict to TestFunctionState objects
                            test_functions = {}
                            if 'test_functions' in module_state_dict:
                                for func_name, func_dict in module_state_dict['test_functions'].items():
                                    test_functions[func_name] = TestFunctionState(**func_dict)
                            
                            # Create ModuleState objects
                            initial_state = TestFunctionState(**module_state_dict['initial_state']) if module_state_dict.get('initial_state') else None
                            current_state = TestFunctionState(**module_state_dict['current_state']) if module_state_dict.get('current_state') else None
                            
                            module_state = ModuleState(
                                initial_state=initial_state,
                                current_state=current_state,
                                test_functions=test_functions
                            )
                            
                            result = TestResult(
                                module_path=result_dict['module_path'],
                                module_state=module_state,
                                errors=result_dict.get('errors', []),
                                warnings=result_dict.get('warnings', [])
                            )
                            results.append(result)
                    
                    data['results'] = results
                
                self.previous_results = TestRunSummary(**data)
                logger.info("Successfully loaded previous results: %d modules, %d tests", 
                           self.previous_results.total_modules, self.previous_results.total_tests)
        except Exception as e:
            logger.error("Error loading previous results: %s", e)
            print(f"Error loading previous results: {e}")
            self.previous_results = None
    
    def _should_skip_module(self, module_path: str) -> tuple[bool, str]:
        """Determine if a module should be skipped based on previous results."""
        logger.debug("Checking if module should be skipped: %s", module_path)
        
        if self.force_run:
            logger.debug("Force run enabled, not skipping module: %s", module_path)
            return False, "Force run enabled"
        
        if not self.previous_results:
            logger.debug("No previous results available, not skipping module: %s", module_path)
            return False, "No previous results"
        
        # Find previous result for this module
        for result in self.previous_results.results:
            if result.module_path == module_path:
                current_state = result.current_state
                
                # Check if all tests passed
                if current_state.failed == 0 and current_state.errors == 0:
                    # Check if recent enough
                    try:
                        from datetime import datetime
                        result_time = datetime.strptime(current_state.timestamp, '%Y-%m-%d %H:%M:%S')
                        current_time = datetime.now()
                        hours_ago = (current_time - result_time).total_seconds() / 3600
                        
                        if hours_ago < self.skip_threshold_hours:
                            logger.debug("Skipping module %s: all tests passed %.1f hours ago", module_path, hours_ago)
                            return True, f"All tests passed {hours_ago:.1f}h ago"
                        else:
                            logger.debug("Not skipping module %s: tests passed %.1f hours ago (threshold: %d)", 
                                       module_path, hours_ago, self.skip_threshold_hours)
                    except Exception as e:
                        logger.debug("Error parsing timestamp for module %s: %s", module_path, e)
                        pass
                else:
                    logger.debug("Not skipping module %s: has failures or errors", module_path)
                
                break
        
        logger.debug("Module %s needs attention", module_path)
        return False, "Module needs attention"
    
    def _create_module_state(self, module_path: str, test_functions: List[TestFunctionState], 
                           total_runtime: float) -> ModuleState:
        """Create a ModuleState from test function results."""
        if not test_functions:
            return ModuleState(
                module_path=module_path,
                test_functions=[],
                total_tests=0,
                passed=0,
                failed=0,
                skipped=0,
                errors=0,
                total_runtime=total_runtime,
                average_runtime=0.0,
                slowest_test="",
                fastest_test="",
                success_rate=0.0,
                timestamp=time.strftime('%Y-%m-%d %H:%M:%S'),
                should_skip_module=False,
                skip_reason="",
                improvement_from_initial=False
            )
        
        # Calculate statistics
        total_tests = len(test_functions)
        passed = sum(1 for t in test_functions if t.status == "passed")
        failed = sum(1 for t in test_functions if t.status == "failed")
        skipped = sum(1 for t in test_functions if t.status == "skipped")
        errors = sum(1 for t in test_functions if t.status == "error")
        
        # Calculate runtimes
        runtimes = [t.runtime for t in test_functions if t.runtime > 0]
        average_runtime = sum(runtimes) / len(runtimes) if runtimes else 0.0
        
        # Find slowest and fastest tests
        if runtimes:
            slowest_idx = max(range(len(runtimes)), key=lambda i: runtimes[i])
            fastest_idx = min(range(len(runtimes)), key=lambda i: runtimes[i])
            slowest_test = test_functions[slowest_idx].function_name
            fastest_test = test_functions[fastest_idx].function_name
        else:
            slowest_test = ""
            fastest_test = ""
        
        success_rate = (passed / total_tests * 100) if total_tests > 0 else 0.0
        
        return ModuleState(
            module_path=module_path,
            test_functions=test_functions,
            total_tests=total_tests,
            passed=passed,
            failed=failed,
            skipped=skipped,
            errors=errors,
            total_runtime=total_runtime,
            average_runtime=average_runtime,
            slowest_test=slowest_test,
            fastest_test=fastest_test,
            success_rate=success_rate,
            timestamp=time.strftime('%Y-%m-%d %H:%M:%S'),
            should_skip_module=False,
            skip_reason="",
            improvement_from_initial=False
        )
    
    def run_all_tests(self):
        """Run all tests with smart skipping and detailed reporting."""
        logger.info("Starting test execution for %d modules", len(self.test_modules))
        print("Loaded previous results from test_results.json")
        print(f"Found {len(self.test_modules)} test modules to evaluate")
        print("=" * 80)
        print()
        
        # Determine which modules to run
        modules_to_run = []
        modules_to_skip = []
        
        logger.debug("Evaluating %d modules for skipping", len(self.test_modules))
        for module_path in self.test_modules:
            should_skip, reason = self._should_skip_module(module_path)
            if should_skip:
                modules_to_skip.append((module_path, reason))
            else:
                modules_to_run.append(module_path)
        
        logger.info("Module evaluation complete: %d to run, %d to skip", len(modules_to_run), len(modules_to_skip))
        
        # Print skipping summary
        if modules_to_skip:
            print(f"SKIPPING {len(modules_to_skip)} modules that are in good shape:")
            for module_path, reason in modules_to_skip:
                print(f"  → {module_path}: {reason}")
            print()
        
        # Print running summary
        if modules_to_run:
            print(f"RUNNING {len(modules_to_run)} modules that need attention:")
            for module_path in modules_to_run:
                should_skip, reason = self._should_skip_module(module_path)
                print(f"  → {module_path}: {reason}")
            print()
            print("=" * 80)
            print()
        
        # Run the modules
        logger.info("Starting execution of %d modules", len(modules_to_run))
        for i, module_path in enumerate(modules_to_run, 1):
            logger.info("Running module %d/%d: %s", i, len(modules_to_run), module_path)
            if self.verbose in ["module", "file", "class", "function"]:
                print(f"[{i}/{len(modules_to_run)}] Testing module: {module_path}")
                print("-" * 60)
            
            result = self._run_test_module(module_path)
            self.results.append(result)
            
            # Print module summary based on verbose level
            state = result.current_state
            logger.info("Module %s completed: %d passed, %d failed, %d errors, %d skipped", 
                       module_path, state.passed, state.failed, state.errors, state.skipped)
            
            if self.verbose == "module":
                # Minimal output for module level
                status = "✓" if state.failed == 0 and state.errors == 0 else "✗"
                print(f"{status} {module_path}: {state.passed} passed, {state.failed} failed, {state.errors} errors")
            else:
                # Detailed output for file/class/function levels
                print(f"Results: {state.passed} passed, {state.failed} failed, {state.skipped} skipped, {state.errors} errors")
                print(f"Runtime: {state.total_runtime:.3f}s total, {state.average_runtime:.3f}s average")
                
                if result.errors:
                    print(f"Errors: {len(result.errors)} issues found")
                
                if result.overall_improvement:
                    print("✓ Module improved from previous run!")
                
                print()
        
        # Print final summary
        logger.info("All test execution completed")
        self._print_final_summary()
    
    def _run_test_module(self, module_path: str) -> TestResult:
        """Run a single test module and collect detailed statistics."""
        logger.debug("Running test module: %s", module_path)
        if self.verbose in ["module", "file", "class", "function"]:
            print(f"Running tests for module: {module_path}")
        
        # Get initial state from previous results if available
        initial_state: Optional[ModuleState] = None
        if self.previous_results:
            for result in self.previous_results.results:
                if result.module_path == module_path:
                    initial_state = result.current_state
                    logger.debug("Found previous state for module %s: %d passed, %d failed", 
                               module_path, initial_state.passed, initial_state.failed)
                    break
        
        # Run the test and collect results
        start_time = time.time()
        errors: List[str] = []
        warnings: List[str] = []
        
        try:
            logger.debug("Executing test module %s with verbose level: %s", module_path, self.verbose)
            # Use hierarchical approach based on verbose level
            if self.verbose == "function":
                # Run individual test functions (most verbose)
                test_functions = self.executor.run_test_file(module_path)
            elif self.verbose == "class":
                # Run test classes (default)
                test_functions = self.executor.run_test_file(module_path)
            elif self.verbose == "file":
                # Run test file
                test_functions = self.executor.run_test_file(module_path)
            else:  # module level
                # Run entire module at once (least verbose)
                cmd = [self.python_path, "-m", "unittest", module_path, "-v"]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
                
                # Parse the output to extract test statistics
                output_lines = result.stdout.split('\n')
                stderr_lines = result.stderr.split('\n')
                
                # If stdout is empty but stderr has test output, use stderr
                if not any("test_" in line for line in output_lines) and any("test_" in line for line in stderr_lines):
                    output_lines = stderr_lines
                    stderr_lines = []
                
                # Parse individual test functions
                test_functions, parse_errors, parse_warnings = self.parser.parse_test_output(output_lines, stderr_lines)
                errors.extend(parse_errors)
                warnings.extend(parse_warnings)
            
            total_runtime = time.time() - start_time
            
            # Show individual function results if requested
            if self.show_function_results and test_functions:
                print(f"  Individual test results for {module_path}:")
                for test_func in test_functions:
                    status_symbol = "✓" if test_func.status == "passed" else "✗" if test_func.status == "failed" else "⚠" if test_func.status == "error" else "⏭" if test_func.status == "skipped" else "?"
                    print(f"    {status_symbol} {test_func.function_name} ({test_func.status}) - {test_func.runtime:.3f}s")
            
            # Create current state
            current_state = self._create_module_state(module_path, test_functions, total_runtime)
            
            # Determine if module improved
            improvement_from_initial = False
            if initial_state:
                improvement_from_initial = (
                    current_state.passed > initial_state.passed or
                    current_state.failed < initial_state.failed or
                    current_state.errors < initial_state.errors
                )
            
            return TestResult(
                module_path=module_path,
                initial_state=initial_state,
                current_state=current_state,
                errors=errors,
                warnings=warnings,
                overall_improvement=improvement_from_initial
            )
            
        except subprocess.TimeoutExpired:
            error_msg = f"Test module {module_path} timed out after 5 minutes"
            logger.error("Test module %s timed out after 5 minutes", module_path)
            errors.append(error_msg)
            print(f"ERROR: {error_msg}")
            
            # Create error state
            current_state = self._create_module_state(module_path, [], time.time() - start_time)
            return TestResult(
                module_path=module_path,
                initial_state=initial_state,
                current_state=current_state,
                errors=errors,
                warnings=warnings,
                overall_improvement=False
            )
        except Exception as e:
            error_msg = f"Error running test module {module_path}: {e}"
            logger.error("Error running test module %s: %s", module_path, e)
            errors.append(error_msg)
            print(f"ERROR: {error_msg}")
            
            # Create error state
            current_state = self._create_module_state(module_path, [], time.time() - start_time)
            return TestResult(
                module_path=module_path,
                initial_state=initial_state,
                current_state=current_state,
                errors=errors,
                warnings=warnings,
                overall_improvement=False
            )
    
    def _print_final_summary(self):
        """Print final summary of test run."""
        if not self.results:
            logger.warning("No test results to summarize")
            print("No test results to summarize.")
            return
        
        total_modules = len(self.results)
        modules_run = len([r for r in self.results if r.current_state.total_tests > 0])
        modules_skipped = total_modules - modules_run
        
        total_tests = sum(r.current_state.total_tests for r in self.results)
        total_passed = sum(r.current_state.passed for r in self.results)
        total_failed = sum(r.current_state.failed for r in self.results)
        total_skipped = sum(r.current_state.skipped for r in self.results)
        total_errors = sum(r.current_state.errors for r in self.results)
        
        success_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0.0
        total_execution_time = sum(r.current_state.total_runtime for r in self.results)
        
        logger.info("Final test summary: %d modules, %d tests, %d passed, %d failed, %d errors, %.1f%% success rate", 
                   total_modules, total_tests, total_passed, total_failed, total_errors, success_rate)
        
        print("=" * 80)
        print("All tests completed!")
        print(f"Results saved to JSON: {self.results_file}")
        print()
        print("FINAL SUMMARY:")
        print(f"Total modules evaluated: {total_modules}")
        print(f"Modules run: {modules_run}")
        print(f"Modules skipped: {modules_skipped}")
        print(f"Total tests: {total_tests}")
        print(f"Passed: {total_passed}")
        print(f"Failed: {total_failed}")
        print(f"Errors: {total_errors}")
        print(f"Success rate: {success_rate:.1f}%")
        print(f"Results saved to {self.results_file}")
    
    def save_results_json(self):
        """Save test results to JSON file."""
        if not self.results:
            logger.warning("No results to save")
            print("No results to save.")
            return
        
        logger.info("Saving %d test results to JSON file: %s", len(self.results), self.results_file)
        
        # Calculate summary statistics
        total_modules = len(self.results)
        modules_run = len([r for r in self.results if r.current_state.total_tests > 0])
        modules_skipped = total_modules - modules_run
        
        total_tests = sum(r.current_state.total_tests for r in self.results)
        total_passed = sum(r.current_state.passed for r in self.results)
        total_failed = sum(r.current_state.failed for r in self.results)
        total_skipped = sum(r.current_state.skipped for r in self.results)
        total_errors = sum(r.current_state.errors for r in self.results)
        
        success_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0.0
        total_execution_time = sum(r.current_state.total_runtime for r in self.results)
        
        # Create summary
        summary = TestRunSummary(
            timestamp=time.strftime('%Y-%m-%d %H:%M:%S'),
            python_executable=self.python_path,
            total_modules=total_modules,
            modules_run=modules_run,
            modules_skipped=modules_skipped,
            total_tests=total_tests,
            total_passed=total_passed,
            total_failed=total_failed,
            total_skipped=total_skipped,
            total_errors=total_errors,
            success_rate=success_rate,
            total_execution_time=total_execution_time,
            results=self.results
        )
        
        # Save to JSON
        try:
            with open(self.results_file, 'w') as f:
                json.dump(summary.__dict__, f, indent=2, default=str)
            logger.info("Successfully saved results to: %s", self.results_file)
            print(f"Results saved to {self.results_file}")
        except Exception as e:
            logger.error("Error saving results to %s: %s", self.results_file, e)
            print(f"Error saving results: {e}")
