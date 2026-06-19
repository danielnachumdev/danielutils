#!/usr/bin/env python3
"""
Tests for 'import X' syntax with lazy loading.

This test suite verifies the behavior of 'import X' syntax
before and after lazy loading setup, with both real and bogus modules.
"""

import unittest
import sys
from danielutils.reflection.module.lazy_module import lazy_import, LazyModule


class TestImportX(unittest.TestCase):
    """Test 'import X' syntax with lazy loading."""

    def setUp(self):
        """Set up test fixtures."""
        # Clear any existing modules from sys.modules
        if 'test_module' in sys.modules:
            del sys.modules['test_module']
        if 'json' in sys.modules:
            del sys.modules['json']

    def tearDown(self):
        """Clean up after tests."""
        if 'test_module' in sys.modules:
            del sys.modules['test_module']
        if 'json' in sys.modules:
            del sys.modules['json']

    def test_import_bogus_module_before_lazy_loading_fails(self):
        """Test that 'import X' fails immediately for bogus modules before lazy loading."""
        with self.assertRaises(ImportError):
            import test_module

    def test_import_bogus_module_after_lazy_loading_succeeds_but_usage_fails(self):
        """Test that 'import X' succeeds for bogus modules after lazy loading, but usage fails."""
        # Set up lazy loading BEFORE import
        lazy_import(
            'test_module',
            'Test module is required',
            'pip install test-module'
        )

        # Import should succeed (no ImportError)
        import test_module
        self.assertIsInstance(test_module, LazyModule)

        # Usage should fail with custom error message
        with self.assertRaises(ImportError) as context:
            test_module.some_function()

        self.assertIn('Test module is required', str(context.exception))
        self.assertIn('pip install test-module', str(context.exception))

    def test_import_real_module_before_lazy_loading_works(self):
        """Test that 'import X' works normally for real modules before lazy loading."""
        # Import should succeed and be the real module
        import json
        self.assertNotIsInstance(json, LazyModule)

        # Usage should work normally
        result = json.loads('{"test": "value"}')
        self.assertEqual(result, {"test": "value"})

    def test_import_real_module_after_lazy_loading_works_normally(self):
        """Test that 'import X' works normally for real modules after lazy loading."""
        # Set up lazy loading for json (which exists)
        lazy_import(
            'json',
            'JSON module is required',
            'pip install json'
        )

        # Import should succeed and be a LazyModule that delegates to the real module
        import json
        self.assertIsInstance(json, LazyModule)

        # Usage should work normally (LazyModule should delegate to real module)
        result = json.loads('{"test": "value"}')
        self.assertEqual(result, {"test": "value"})

    def test_import_bogus_module_attribute_access_fails(self):
        """Test that attribute access on bogus module fails with custom error."""
        # Set up lazy loading BEFORE import
        lazy_import(
            'test_module',
            'Test module is required',
            'pip install test-module'
        )

        # Import should succeed
        import test_module
        self.assertIsInstance(test_module, LazyModule)

        # Attribute access should fail with custom error
        with self.assertRaises(ImportError) as context:
            _ = test_module.some_attribute

        self.assertIn('Test module is required', str(context.exception))

    def test_import_bogus_module_method_call_fails(self):
        """Test that method calls on bogus module fail with custom error."""
        # Set up lazy loading BEFORE import
        lazy_import(
            'test_module',
            'Test module is required',
            'pip install test-module'
        )

        # Import should succeed
        import test_module
        self.assertIsInstance(test_module, LazyModule)

        # Method call should fail with custom error
        with self.assertRaises(ImportError) as context:
            test_module.some_class().some_method()

        self.assertIn('Test module is required', str(context.exception))

    def test_import_bogus_module_nested_attribute_access_fails(self):
        """Test that nested attribute access on bogus module fails with custom error."""
        # Set up lazy loading BEFORE import
        lazy_import(
            'test_module',
            'Test module is required',
            'pip install test-module'
        )

        # Import should succeed
        import test_module
        self.assertIsInstance(test_module, LazyModule)

        # Nested attribute access should fail with custom error
        with self.assertRaises(ImportError) as context:
            test_module.some_class.some_method.some_attribute

        self.assertIn('Test module is required', str(context.exception))


if __name__ == '__main__':
    unittest.main()
