"""
Core test runner modules.

This package contains the core functionality split by responsibility:
- discovery: Test discovery and structure analysis
- execution: Test execution hierarchy
- parser: Output parsing and result processing
- runner: Main TestRunner orchestration
- types: Type definitions and data structures
"""

from .runner import TestRunner

# Define VerboseLevel here since it's a simple type alias
from typing import Literal
VerboseLevel = Literal["module", "file", "class", "function"]

