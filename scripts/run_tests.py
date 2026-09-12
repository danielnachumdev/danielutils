#!/usr/bin/env python3
"""
Test Runner - Smart test execution with hierarchical control and smart skipping.

Usage:
    python scripts/run_tests.py run_tests --help
    python scripts/run_tests.py run_tests --test_name tests.abstractions.db.test_in_memory_database --verbose --show_function_results
    python scripts/run_tests.py run_tests --force --show_function_results
"""

from danielutils.tools.unittest_test_runner.cli import main

if __name__ == "__main__":
    main()
