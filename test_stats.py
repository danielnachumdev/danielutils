#!/usr/bin/env python3
"""Test script to demonstrate the enhanced FileInfo and FunctionInfo stats functionality."""

import sys
import json
from pathlib import Path
from danielutils.reflection.info_classes.file_info import FileInfo
from danielutils.reflection.info_classes.function_info import FunctionInfo


def test_function_stats():
    """Test function statistics on a simple function."""
    print("Testing FunctionInfo stats...")

    # Test with a simple function
    def sample_function(x: int, y: str = "default") -> bool:
        """A sample function for testing."""
        if x > 10:
            return True
        elif x < 0:
            return False
        else:
            return y == "default"

    try:
        # Create FunctionInfo instance
        func_info = FunctionInfo(sample_function, type(sample_function))

        # Get statistics
        stats = func_info.stats

        print(f"Function: {func_info.name}")
        print(f"Overall Score: {stats.overall_score:.2f}")
        print(f"Quality: {stats.quality_assessment}")
        print(
            f"Cyclomatic Complexity: {stats.complexity.cyclomatic_complexity}")
        print(f"Max Indentation: {stats.complexity.max_indentation_level}")
        print(f"Total Lines: {stats.code.total_lines}")
        print(f"Has Docstring: {stats.code.has_docstring}")
        print(f"Typing Score: {stats.typing.typing_score:.2f}")
        print(f"Is Fully Typed: {stats.typing.is_fully_typed}")
        print()

    except Exception as e:
        print(f"Error testing function stats: {e}")
        print()


def test_file_stats(target_file):
    """Test file statistics on the specified target file."""
    try:
        # Analyze the target file
        file_info = FileInfo(target_file)

        # Get statistics in JSON-serializable format
        json_stats = file_info.get_stats_dict()

        # Print JSON to STDOUT
        print(json.dumps(json_stats, indent=2))

    except Exception as e:
        error_json = {
            "error": str(e),
            "file_path": target_file
        }
        print(json.dumps(error_json, indent=2), file=sys.stderr)
        sys.exit(1)


def main():
    """Main function to handle command line arguments and run the appropriate test."""
    if len(sys.argv) != 2:
        print("Usage: python test_stats.py <target_file>")
        print("Example: python test_stats.py danielutils/reflection/info_classes/function_info.py")
        sys.exit(1)

    target_file = sys.argv[1]

    # Check if file exists
    if not Path(target_file).exists():
        error_json = {
            "error": f"File not found: {target_file}",
            "file_path": target_file
        }
        print(json.dumps(error_json, indent=2), file=sys.stderr)
        sys.exit(1)

    # Run file stats analysis and output JSON to STDOUT
    test_file_stats(target_file)


if __name__ == "__main__":
    main()
