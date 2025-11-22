"""
Tests for the TestDiscoveryService class.
"""
import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
import tempfile
import os

from danielutils.tools.unittest_test_runner.core.discovery import TestDiscoveryService
from danielutils.tools.unittest_test_runner.models import TestDiscovery
from tests.test_tools.base import BaseToolTest


class TestTestDiscoveryService(BaseToolTest):
    """Test cases for TestDiscoveryService."""
    
    def setUp(self):
        """Set up test fixtures."""
        super().setUp()
        self.python_path = "python"
        self.verbose = "class"
        self.discovery_service = TestDiscoveryService(self.python_path, self.verbose)
    
    def test_init(self):
        """Test TestDiscoveryService initialization."""
        self.assertEqual(self.discovery_service._python_path, self.python_path)
        self.assertEqual(self.discovery_service._verbose, self.verbose)
    
    @patch('danielutils.tools.unittest_test_runner.core.discovery.Path.rglob')
    def test_discover_test_modules(self, mock_rglob):
        """Test discovering test modules."""
        # Mock test files - only include files that start with test_
        mock_files = [
            Path("tests/test_module1.py"),
            Path("tests/test_module2.py"),
            Path("tests/subdir/test_module3.py"),
        ]
        mock_rglob.return_value = mock_files
        
        # Mock Path.exists to return True for tests directory
        with patch.object(Path, 'exists', return_value=True):
            modules = self.discovery_service.discover_test_modules()
        
        # Should find 3 test modules
        self.assertEqual(len(modules), 3)
        self.assertIn("tests.test_module1", modules)
        self.assertIn("tests.test_module2", modules)
        self.assertIn("tests.subdir.test_module3", modules)
    
    @patch('danielutils.tools.unittest_test_runner.core.discovery.subprocess.run')
    def test_discover_test_structure(self, mock_run):
        """Test discovering test structure from modules."""
        test_modules = [
            "tests.test_module1",
            "tests.test_module2",
        ]
        
        # Mock the subprocess.run call
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = (
                "test_module1.TestClass1.test_function1\n"
                "test_module1.TestClass1.test_function2\n"
                "test_module1.TestClass2.test_function3\n"
                "test_module2.TestClass3.test_function4\n"
            )
        mock_result.stderr = ""
        mock_run.return_value = mock_result
        
        discovery = self.discovery_service.discover_test_structure(test_modules)
        
        self.assertIsInstance(discovery, TestDiscovery)
        self.assertEqual(discovery.total_modules, 2)
        self.assertIn("tests.test_module1", discovery.modules)
        self.assertIn("tests.test_module2", discovery.modules)
    
    def test_parse_target_module_only(self):
        """Test parsing target with module only."""
        target = "tests.test_module"
        module, test_class, test_function = self.discovery_service.parse_target(target)
        
        self.assertEqual(module, "tests.test_module")
        self.assertIsNone(test_class)
        self.assertIsNone(test_function)
    
    def test_parse_target_module_and_class(self):
        """Test parsing target with module and class."""
        target = "tests.test_module.TestClass"
        module, test_class, test_function = self.discovery_service.parse_target(target)
        
        self.assertEqual(module, "tests.test_module")
        self.assertEqual(test_class, "TestClass")
        self.assertIsNone(test_function)
    
    def test_parse_target_full_path(self):
        """Test parsing target with full path."""
        target = "tests.test_module.TestClass.test_function"
        module, test_class, test_function = self.discovery_service.parse_target(target)
        
        self.assertEqual(module, "tests.test_module")
        self.assertEqual(test_class, "TestClass")
        self.assertEqual(test_function, "test_function")
    
    def test_parse_target_invalid_format(self):
        """Test parsing invalid target format."""
        target = "invalid.target.too.many.parts"
        module, test_class, test_function = self.discovery_service.parse_target(target)
        
        # Should return tuple with parsed components
        self.assertEqual(module, "invalid.target")
        self.assertEqual(test_class, "too")
        self.assertEqual(test_function, "parts")
    
    def test_create_focused_discovery(self):
        """Test creating focused discovery from target."""
        # Create a mock full discovery
        full_discovery = TestDiscovery(
            modules=["tests.test_module1", "tests.test_module2"],
            classes={
                "tests.test_module1": ["TestClass1", "TestClass2"],
                "tests.test_module2": ["TestClass3"]
            },
            functions={
                "tests.test_module1.TestClass1": ["test_function1", "test_function2"],
                "tests.test_module1.TestClass2": ["test_function3"],
                "tests.test_module2.TestClass3": ["test_function4"]
            },
            total_functions=4,
            total_classes=3,
            total_modules=2
        )
        
        # Test module-only target
        target_module, target_class, target_function = self.discovery_service.parse_target("tests.test_module1")
        focused = self.discovery_service.create_focused_discovery(target_module, target_class, target_function, full_discovery)
        
        self.assertEqual(focused.total_modules, 1)
        self.assertIn("tests.test_module1", focused.modules)
        self.assertNotIn("tests.test_module2", focused.modules)
        
        # Test class-only target
        target_module, target_class, target_function = self.discovery_service.parse_target("tests.test_module1.TestClass1")
        focused = self.discovery_service.create_focused_discovery(target_module, target_class, target_function, full_discovery)
        
        self.assertEqual(focused.total_modules, 1)
        self.assertEqual(len(focused.classes["tests.test_module1"]), 1)
        self.assertIn("TestClass1", focused.classes["tests.test_module1"])
        self.assertNotIn("TestClass2", focused.classes["tests.test_module1"])


if __name__ == '__main__':
    unittest.main()
