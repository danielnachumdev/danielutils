"""
Command-line interface for the test runner using Google Fire.
"""

import logging
import fire
from typing import Optional, Literal
from .core import TestRunner, VerboseLevel

logger = logging.getLogger(__name__)


def run_tests(python_path: Optional[str] = None,
              results_file: str = "test_results.json",
              skip_threshold: int = 24,
              force: bool = False,
              test_name: Optional[str] = None,
              target: Optional[str] = None,
              verbose: VerboseLevel = "class",
              show_function_results: bool = False):
    """
    Run tests with smart skipping and detailed reporting.
    
    Args:
        python_path: Path to Python executable to use for running tests (defaults to current Python)
        results_file: JSON file to store/load results (default: test_results.json)
        skip_threshold: Hours after which to re-run previously passing tests (default: 24)
        force: Force run all tests, ignoring previous results
        test_name: Run only a specific test module (e.g., tests.abstractions.db.test_in_memory_database)
        target: unittest dot-notation target (e.g., tests.module.class.function)
        verbose: Verbose level - module/file/class/function (default: class)
        show_function_results: Show pass/fail status for each individual test function within modules
    """
    logger.info("Starting test run with parameters: python_path=%s, results_file=%s, skip_threshold=%d, force=%s, target=%s, verbose=%s", 
                python_path, results_file, skip_threshold, force, target, verbose)
    
    runner = TestRunner(
        python_path=python_path,
        results_file=results_file,
        skip_threshold_hours=skip_threshold,
        force_run=force,
        test_name=test_name,
        target=target,
        verbose=verbose,
        show_function_results=show_function_results
    )

    try:
        logger.info("Executing all tests")
        runner.run_all_tests()
        logger.info("Saving results to JSON file: %s", results_file)
        runner.save_results_json()
        logger.info("Test run completed successfully")
    except KeyboardInterrupt:
        logger.warning("Test run interrupted by user")
        print("\nTest run interrupted by user.")
    except Exception as e:
        logger.error("Error during test run: %s", e)
        print(f"Error during test run: {e}")
        raise


def main():
    """Main entry point for the CLI."""
    logger.info("Starting CLI main entry point")
    fire.Fire(run_tests)


if __name__ == "__main__":
    main()
