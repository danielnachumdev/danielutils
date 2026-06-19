#!/usr/bin/env python3
"""
Tests for 'from X import Y' syntax with lazy loading.

This test suite verifies the behavior of 'from X import Y' syntax
before and after lazy loading setup, with both real and bogus modules.
"""

import unittest
import sys
from danielutils.reflection.module.lazy_module import lazy_import, LazyModule


class TestFromXImportY(unittest.TestCase):
    """Test 'from X import Y' syntax with lazy loading."""

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

    def test_from_import_bogus_module_before_lazy_loading_fails(self):
        """Test that 'from X import Y' fails immediately for bogus modules before lazy loading."""
        with self.assertRaises(ImportError):
            from test_module import some_function

    def test_from_import_bogus_module_after_lazy_loading_fails(self):
        """Test that 'from X import Y' fails for bogus modules after lazy loading."""
        # Set up lazy loading BEFORE import
        lazy_import(
            'test_module',
            'Test module is required',
            'pip install test-module'
        )

        # Import should fail because test_module doesn't exist
        with self.assertRaises(ImportError):
            from test_module import some_function

    def test_from_import_real_module_before_lazy_loading_works(self):
        """Test that 'from X import Y' works normally for real modules before lazy loading."""
        # Import should succeed and be the real function
        from json import loads
        # loads should be a real function
        self.assertIsInstance(loads, type(lambda: None))

        # Usage should work normally
        result = loads('{"test": "value"}')
        self.assertEqual(result, {"test": "value"})

    def test_from_import_real_module_after_lazy_loading_works_normally(self):
        """Test that 'from X import Y' works normally for real modules after lazy loading."""
        # Set up lazy loading for json (which exists)
        lazy_import(
            'json',
            'JSON module is required',
            'pip install json'
        )

        # Import should succeed and be the real function (LazyModule delegates to real module)
        from json import loads
        # loads should be a real function
        self.assertIsInstance(loads, type(lambda: None))

        # Usage should work normally
        result = loads('{"test": "value"}')
        self.assertEqual(result, {"test": "value"})

    def test_from_import_bogus_module_class_instantiation_fails(self):
        """Test that class instantiation from bogus module fails."""
        # Set up lazy loading BEFORE import
        lazy_import(
            'test_module',
            'Test module is required',
            'pip install test-module'
        )

        # Import should fail because test_module doesn't exist
        with self.assertRaises(ImportError):
            from test_module import SomeClass

    def test_from_import_real_module_class_instantiation_works(self):
        """Test that class instantiation from real module works normally."""
        # Set up lazy loading for json (which exists)
        lazy_import(
            'json',
            'JSON module is required',
            'pip install json'
        )

        # Import should succeed and be the real class (LazyModule delegates to real module)
        from json import JSONDecoder
        # JSONDecoder should be a real class
        self.assertIsInstance(JSONDecoder, type)

        # Class instantiation should work normally
        decoder = JSONDecoder()
        result = decoder.decode('{"test": "value"}')
        self.assertEqual(result, {"test": "value"})


if __name__ == '__main__':
    unittest.main()
