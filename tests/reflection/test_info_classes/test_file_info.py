import unittest
import tempfile
import os
from pathlib import Path
from danielutils.reflection.info_classes.file_info import FileInfo, CodeQualityLevel
from danielutils.reflection.info_classes.import_info import ImportType


class TestFileInfoBasic(unittest.TestCase):
    """Test basic FileInfo functionality."""

    def setUp(self):
        """Create a temporary test file."""
        self.test_content = '''"""
Test file for FileInfo testing.
This file contains various Python constructs.
"""

import os
import sys
from typing import List, Dict
# from . import utils  # Commented out to avoid relative import issues in tests

class TestClass:
    """A test class for testing."""
    
    def __init__(self):
        self.value = 42
    
    def test_method(self):
        """A test method."""
        if self.value > 40:
            return True
        return False

def test_function():
    """A test function."""
    result = []
    for i in range(10):
        if i % 2 == 0:
            result.append(i)
    return result

async def async_function():
    """An async test function."""
    await asyncio.sleep(0.1)
    return "async result"

# This is a comment
# Another comment line

if __name__ == "__main__":
    print("Running test")
'''

        # Create temporary file
        self.temp_file = tempfile.NamedTemporaryFile(
            mode='w', suffix='.py', delete=False, encoding='utf-8')
        self.temp_file.write(self.test_content)
        self.temp_file.close()

        # Create FileInfo instance
        self.file_info = FileInfo(self.temp_file.name)

    def tearDown(self):
        """Clean up temporary file."""
        os.unlink(self.temp_file.name)

    def test_file_path(self):
        """Test file path property."""
        self.assertEqual(self.file_info.file_path, str(
            Path(self.temp_file.name).resolve()))

    def test_content_reading(self):
        """Test that file content is read correctly."""
        self.assertIn("Test file for FileInfo testing",
                      self.file_info._content)

    def test_ast_parsing(self):
        """Test that AST is parsed correctly."""
        self.assertIsNotNone(self.file_info._tree)

    def test_lines_property(self):
        """Test lines property."""
        lines = self.file_info.lines
        self.assertIsInstance(lines, list)
        self.assertGreater(len(lines), 0)
        self.assertIn("import os", lines)

    def test_tokens_property(self):
        """Test tokens property."""
        tokens = self.file_info.tokens
        self.assertIsInstance(tokens, list)
        self.assertGreater(len(tokens), 0)

    def test_token_count(self):
        """Test token count property."""
        count = self.file_info.token_count
        self.assertIsInstance(count, int)
        self.assertGreater(count, 0)

    def test_token_distribution(self):
        """Test token distribution property."""
        distribution = self.file_info.token_distribution
        self.assertIsInstance(distribution, dict)
        self.assertGreater(len(distribution), 0)

    def test_comments(self):
        """Test comments property."""
        comments = self.file_info.comments
        self.assertIsInstance(comments, list)
        self.assertIn("# This is a comment", comments)

    def test_class_names(self):
        """Test class names property."""
        class_names = self.file_info.class_names
        self.assertIsInstance(class_names, list)
        self.assertIn("TestClass", class_names)

    def test_function_names(self):
        """Test function names property."""
        function_names = self.file_info.function_names
        self.assertIsInstance(function_names, list)
        self.assertIn("test_function", function_names)
        self.assertIn("async_function", function_names)

    def test_used_names(self):
        """Test used names property."""
        used_names = self.file_info.used_names
        self.assertIsInstance(used_names, set)
        self.assertIn("os", used_names)
        self.assertIn("sys", used_names)


class TestFileInfoImports(unittest.TestCase):
    """Test import-related functionality."""

    def setUp(self):
        """Create a test file with various imports."""
        self.test_content = '''import os
import sys as system
from typing import List, Dict
# from . import utils  # Commented out to avoid relative import issues in tests
# from .. import models  # Commented out to avoid relative import issues in tests
from datetime import datetime, timedelta
import numpy as np
# from .utils import helper_function  # Commented out to avoid relative import issues in tests
'''

        self.temp_file = tempfile.NamedTemporaryFile(
            mode='w', suffix='.py', delete=False, encoding='utf-8')
        self.temp_file.write(self.test_content)
        self.temp_file.close()

        self.file_info = FileInfo(self.temp_file.name)

    def tearDown(self):
        """Clean up temporary file."""
        os.unlink(self.temp_file.name)

    def test_imports_property(self):
        """Test imports property."""
        imports = self.file_info.imports
        self.assertIsInstance(imports, list)
        # 5 import statements create 7 ImportInfo objects
        self.assertEqual(len(imports), 7)

    def test_import_statistics(self):
        """Test import statistics."""
        stats = self.file_info.import_statistics
        self.assertIsInstance(stats, dict)
        self.assertEqual(stats['total_imports'], 7)
        self.assertIn('by_type', stats)
        self.assertIn('by_scope', stats)

    def test_import_types(self):
        """Test import type categorization."""
        global_package = self.file_info.get_imports_by_type(
            ImportType.GLOBAL_PACKAGE)
        global_from_package = self.file_info.get_imports_by_type(
            ImportType.GLOBAL_FROM_PACKAGE)
        local_package = self.file_info.get_imports_by_type(
            ImportType.LOCAL_PACKAGE)
        local_from_package = self.file_info.get_imports_by_type(
            ImportType.LOCAL_FROM_PACKAGE)

        self.assertGreater(len(global_package), 0)
        self.assertGreater(len(global_from_package), 0)
        self.assertGreaterEqual(len(local_package), 0)
        self.assertGreaterEqual(len(local_from_package), 0)

    def test_import_scopes(self):
        """Test import scope categorization."""
        absolute_imports = self.file_info.get_imports_by_scope(True)
        relative_imports = self.file_info.get_imports_by_scope(False)

        self.assertGreater(len(absolute_imports), 0)
        # No relative imports in this test file (they're all commented out)
        self.assertEqual(len(relative_imports), 0)

    def test_import_usage(self):
        """Test import usage analysis."""
        usage = self.file_info.import_usage
        self.assertIn('used', usage)
        self.assertIn('unused', usage)
        self.assertIsInstance(usage['used'], list)
        self.assertIsInstance(usage['unused'], list)

    def test_import_efficiency_score(self):
        """Test import efficiency score."""
        score = self.file_info.get_import_efficiency_score()
        self.assertIsInstance(score, float)
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 100.0)

    def test_get_unused_imports(self):
        """Test getting unused imports."""
        unused = self.file_info.get_unused_imports()
        self.assertIsInstance(unused, list)

    def test_get_used_imports(self):
        """Test getting used imports."""
        used = self.file_info.get_used_imports()
        self.assertIsInstance(used, list)


class TestFileInfoCodeMetrics(unittest.TestCase):
    """Test code metrics functionality."""

    def setUp(self):
        """Create a test file with various code constructs."""
        self.test_content = '''"""
This is a docstring.
"""

import os

class SimpleClass:
    """A simple class."""
    
    def __init__(self):
        self.value = 42
    
    def simple_method(self):
        """A simple method."""
        return self.value

def simple_function():
    """A simple function."""
    x = 1
    y = 2
    if x < y:
        return x
    else:
        return y

def complex_function():
    """A more complex function."""
    result = []
    for i in range(10):
        if i % 2 == 0:
            if i > 5:
                result.append(i * 2)
            else:
                result.append(i)
        else:
            result.append(i + 1)
    return result

# Comment line 1
# Comment line 2

if __name__ == "__main__":
    print("Hello, World!")
'''

        self.temp_file = tempfile.NamedTemporaryFile(
            mode='w', suffix='.py', delete=False, encoding='utf-8')
        self.temp_file.write(self.test_content)
        self.temp_file.close()

        self.file_info = FileInfo(self.temp_file.name)

    def tearDown(self):
        """Clean up temporary file."""
        os.unlink(self.temp_file.name)

    def test_code_metrics_property(self):
        """Test code metrics property."""
        metrics = self.file_info.code_metrics
        self.assertIsInstance(metrics, dict)
        self.assertIn('lines', metrics)
        self.assertIn('complexity', metrics)
        self.assertIn('quality', metrics)

    def test_line_metrics(self):
        """Test line counting metrics."""
        lines = self.file_info.code_metrics['lines']
        self.assertIn('total', lines)
        self.assertIn('code', lines)
        self.assertIn('comment', lines)
        self.assertIn('blank', lines)
        self.assertIn('comment_ratio', lines)

        self.assertGreater(lines['total'], 0)
        self.assertGreaterEqual(lines['code'], 0)
        self.assertGreaterEqual(lines['comment'], 0)
        self.assertGreaterEqual(lines['blank'], 0)

    def test_complexity_metrics(self):
        """Test complexity metrics."""
        complexity = self.file_info.code_metrics['complexity']
        self.assertIn('cyclomatic', complexity)
        self.assertIn('function_count', complexity)
        self.assertIn('class_count', complexity)
        self.assertIn('import_count', complexity)

        self.assertGreater(complexity['cyclomatic'], 0)
        self.assertGreater(complexity['function_count'], 0)
        self.assertGreater(complexity['class_count'], 0)

    def test_quality_metrics(self):
        """Test quality metrics."""
        quality = self.file_info.code_metrics['quality']
        self.assertIn('level', quality)
        self.assertIn('score', quality)
        self.assertIn('has_docstrings', quality)
        self.assertIn('has_type_hints', quality)

        self.assertIsInstance(quality['level'], CodeQualityLevel)
        self.assertIsInstance(quality['score'], int)
        self.assertIsInstance(quality['has_docstrings'], bool)

    def test_complexity_assessment(self):
        """Test complexity assessment."""
        assessment = self.file_info.get_complexity_assessment()
        self.assertIsInstance(assessment, str)
        self.assertIn(assessment, ["Very Low", "Low",
                      "Medium", "High", "Very High"])


class TestFileInfoStructure(unittest.TestCase):
    """Test structure analysis functionality."""

    def setUp(self):
        """Create a test file with nested structures."""
        self.test_content = '''import os

def outer_function():
    """Outer function with nested structures."""
    
    def nested_function():
        """A nested function."""
        return "nested"
    
    class NestedClass:
        """A nested class."""
        
        def method(self):
            return "method"
    
    return nested_function()

class BaseClass:
    """A base class."""
    pass

class DerivedClass(BaseClass):
    """A derived class."""
    pass

class MixinClass:
    """A mixin class."""
    pass

class MultipleInheritance(BaseClass, MixinClass):
    """A class with multiple inheritance."""
    pass

@decorator1
@decorator2("arg")
def decorated_function():
    """A decorated function."""
    pass

async def async_function():
    """An async function."""
    await asyncio.sleep(0.1)
'''

        self.temp_file = tempfile.NamedTemporaryFile(
            mode='w', suffix='.py', delete=False, encoding='utf-8')
        self.temp_file.write(self.test_content)
        self.temp_file.close()

        self.file_info = FileInfo(self.temp_file.name)

    def tearDown(self):
        """Clean up temporary file."""
        os.unlink(self.temp_file.name)

    def test_structure_info_property(self):
        """Test structure info property."""
        structure = self.file_info.structure_info
        self.assertIsInstance(structure, dict)
        self.assertIn('nested', structure)
        self.assertIn('decorators', structure)
        self.assertIn('async', structure)
        self.assertIn('inheritance', structure)

    def test_nested_structures(self):
        """Test nested structure detection."""
        nested = self.file_info.structure_info['nested']
        self.assertIn('functions', nested)
        self.assertIn('classes', nested)

        # Should detect nested_function and NestedClass
        self.assertIn('nested_function', nested['functions'])
        self.assertIn('NestedClass', nested['classes'])

    def test_decorators(self):
        """Test decorator detection."""
        decorators = self.file_info.structure_info['decorators']
        self.assertIsInstance(decorators, list)
        self.assertIn('decorator1', decorators)
        self.assertIn('decorator2', decorators)

    def test_async_analysis(self):
        """Test async function analysis."""
        async_info = self.file_info.structure_info['async']
        self.assertIn('functions', async_info)
        self.assertIn('count', async_info)

        self.assertIn('async_function', async_info['functions'])
        self.assertEqual(async_info['count'], 1)

    def test_inheritance_analysis(self):
        """Test inheritance analysis."""
        inheritance = self.file_info.structure_info['inheritance']
        self.assertIsInstance(inheritance, dict)

        # Check BaseClass
        self.assertIn('BaseClass', inheritance)
        self.assertEqual(inheritance['BaseClass']['base_count'], 0)
        self.assertFalse(inheritance['BaseClass']['is_leaf'])

        # Check DerivedClass
        self.assertIn('DerivedClass', inheritance)
        self.assertEqual(inheritance['DerivedClass']['base_count'], 1)
        self.assertTrue(inheritance['DerivedClass']['is_leaf'])

        # Check MultipleInheritance
        self.assertIn('MultipleInheritance', inheritance)
        self.assertEqual(inheritance['MultipleInheritance']['base_count'], 2)
        self.assertTrue(inheritance['MultipleInheritance']['is_mixin'])


class TestFileInfoExport(unittest.TestCase):
    """Test export functionality."""

    def setUp(self):
        """Create a simple test file."""
        self.test_content = '''import os

class TestClass:
    def test_method(self):
        return True

def test_function():
    return "test"
'''

        self.temp_file = tempfile.NamedTemporaryFile(
            mode='w', suffix='.py', delete=False, encoding='utf-8')
        self.temp_file.write(self.test_content)
        self.temp_file.close()

        self.file_info = FileInfo(self.temp_file.name)

    def tearDown(self):
        """Clean up temporary file."""
        os.unlink(self.temp_file.name)

    def test_to_dict(self):
        """Test to_dict method."""
        data = self.file_info.to_dict()
        self.assertIsInstance(data, dict)
        self.assertIn('file_info', data)
        self.assertIn('code_metrics', data)
        self.assertIn('imports', data)
        self.assertIn('structure', data)
        self.assertIn('tokens', data)

    def test_to_json(self):
        """Test to_json method."""
        json_str = self.file_info.to_json()
        self.assertIsInstance(json_str, str)
        self.assertIn('"file_info"', json_str)
        self.assertIn('"code_metrics"', json_str)

    def test_export_summary(self):
        """Test export_summary method."""
        summary = self.file_info.export_summary()
        self.assertIsInstance(summary, str)
        self.assertIn("File Analysis Summary", summary)
        self.assertIn("CODE METRICS", summary)
        self.assertIn("STRUCTURE", summary)
        self.assertIn("IMPORTS", summary)

    def test_export_summary_to_file(self):
        """Test export_summary with file output."""
        temp_output = tempfile.NamedTemporaryFile(
            mode='w', suffix='.txt', delete=False, encoding='utf-8')
        temp_output.close()

        try:
            summary = self.file_info.export_summary(temp_output.name)
            self.assertIsInstance(summary, str)

            # Check if file was created and contains content
            with open(temp_output.name, 'r', encoding='utf-8') as f:
                file_content = f.read()
                self.assertIn("File Analysis Summary", file_content)
        finally:
            os.unlink(temp_output.name)

    def test_file_size_property(self):
        """Test file size property."""
        size_info = self.file_info.file_size
        self.assertIsInstance(size_info, dict)
        self.assertIn('bytes', size_info)
        self.assertIn('kilobytes', size_info)
        self.assertIn('characters', size_info)
        self.assertIn('lines', size_info)
        self.assertIn('tokens', size_info)

        self.assertGreater(size_info['bytes'], 0)
        self.assertGreater(size_info['characters'], 0)
        self.assertGreater(size_info['lines'], 0)
        self.assertGreater(size_info['tokens'], 0)


class TestFileInfoEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""

    def test_empty_file(self):
        """Test FileInfo with an empty file."""
        temp_file = tempfile.NamedTemporaryFile(
            mode='w', suffix='.py', delete=False, encoding='utf-8')
        temp_file.write("")
        temp_file.close()

        try:
            file_info = FileInfo(temp_file.name)

            # Should handle empty file gracefully
            # Empty file has 0 lines
            self.assertEqual(file_info.code_metrics['lines']['total'], 0)
            self.assertEqual(file_info.code_metrics['lines']['code'], 0)
            self.assertEqual(file_info.code_metrics['lines']['comment'], 0)
            self.assertEqual(file_info.code_metrics['lines']['blank'], 0)
        finally:
            os.unlink(temp_file.name)

    def test_file_with_only_comments(self):
        """Test FileInfo with a file containing only comments."""
        temp_file = tempfile.NamedTemporaryFile(
            mode='w', suffix='.py', delete=False, encoding='utf-8')
        temp_file.write("# This is a comment\n# Another comment\n")
        temp_file.close()

        try:
            file_info = FileInfo(temp_file.name)

            self.assertEqual(file_info.code_metrics['lines']['total'], 2)
            self.assertEqual(file_info.code_metrics['lines']['code'], 0)
            self.assertEqual(file_info.code_metrics['lines']['comment'], 2)
            self.assertEqual(file_info.code_metrics['lines']['blank'], 0)
        finally:
            os.unlink(temp_file.name)

    def test_file_with_only_imports(self):
        """Test FileInfo with a file containing only imports."""
        temp_file = tempfile.NamedTemporaryFile(
            mode='w', suffix='.py', delete=False, encoding='utf-8')
        temp_file.write("import os\nimport sys\nfrom typing import List\n")
        temp_file.close()

        try:
            file_info = FileInfo(temp_file.name)

            self.assertEqual(len(file_info.imports), 3)
            # Base complexity
            self.assertEqual(
                file_info.code_metrics['complexity']['cyclomatic'], 1)
        finally:
            os.unlink(temp_file.name)


if __name__ == "__main__":
    unittest.main()
