import unittest
import ast
from danielutils.reflection.info_classes.import_info import ImportInfo, ImportType


class TestImportType(unittest.TestCase):
    """Test cases for ImportType enum."""

    def test_import_type_values(self):
        """Test that ImportType enum has the expected values."""
        self.assertEqual(ImportType.GLOBAL_PACKAGE.value, "global_package")
        self.assertEqual(ImportType.GLOBAL_FROM_PACKAGE.value,
                         "global_from_package")
        self.assertEqual(ImportType.LOCAL_PACKAGE.value, "local_package")
        self.assertEqual(ImportType.LOCAL_FROM_PACKAGE.value,
                         "local_from_package")


class TestImportInfo(unittest.TestCase):
    """Test cases for ImportInfo class."""

    def test_constructor_global_package(self):
        """Test ImportInfo constructor with global package import."""
        import_info = ImportInfo(
            import_type=ImportType.GLOBAL_PACKAGE,
            is_absolute=True,
            module_name="os",
            imported_object=None,
            alias=None,
            relative_level=0
        )

        self.assertEqual(import_info.import_type, ImportType.GLOBAL_PACKAGE)
        self.assertTrue(import_info.is_absolute)
        self.assertFalse(import_info.is_relative)
        self.assertEqual(import_info.module_name, "os")
        self.assertIsNone(import_info.imported_object)
        self.assertIsNone(import_info.alias)
        self.assertEqual(import_info.relative_level, 0)
        self.assertEqual(import_info.effective_name, "os")

    def test_constructor_global_from_package(self):
        """Test ImportInfo constructor with global from package import."""
        import_info = ImportInfo(
            import_type=ImportType.GLOBAL_FROM_PACKAGE,
            is_absolute=True,
            module_name="sys",
            imported_object="version_info",
            alias="ver",
            relative_level=0
        )

        self.assertEqual(import_info.import_type,
                         ImportType.GLOBAL_FROM_PACKAGE)
        self.assertTrue(import_info.is_absolute)
        self.assertEqual(import_info.module_name, "sys")
        self.assertEqual(import_info.imported_object, "version_info")
        self.assertEqual(import_info.alias, "ver")
        self.assertEqual(import_info.effective_name, "ver")

    def test_constructor_local_package(self):
        """Test ImportInfo constructor with local package import."""
        import_info = ImportInfo(
            import_type=ImportType.LOCAL_PACKAGE,
            is_absolute=False,
            module_name="utils",
            imported_object=None,
            alias=None,
            relative_level=1
        )

        self.assertEqual(import_info.import_type, ImportType.LOCAL_PACKAGE)
        self.assertFalse(import_info.is_absolute)
        self.assertTrue(import_info.is_relative)
        self.assertEqual(import_info.module_name, "utils")
        self.assertEqual(import_info.relative_level, 1)
        self.assertEqual(import_info.effective_name, "utils")

    def test_constructor_local_from_package(self):
        """Test ImportInfo constructor with local from package import."""
        import_info = ImportInfo(
            import_type=ImportType.LOCAL_FROM_PACKAGE,
            is_absolute=False,
            module_name="models",
            imported_object="User",
            alias=None,
            relative_level=2
        )

        self.assertEqual(import_info.import_type,
                         ImportType.LOCAL_FROM_PACKAGE)
        self.assertFalse(import_info.is_absolute)
        self.assertEqual(import_info.module_name, "models")
        self.assertEqual(import_info.imported_object, "User")
        self.assertEqual(import_info.relative_level, 2)
        self.assertEqual(import_info.effective_name, "User")

    def test_effective_name_with_alias(self):
        """Test effective_name property when alias is provided."""
        import_info = ImportInfo(
            import_type=ImportType.GLOBAL_PACKAGE,
            is_absolute=True,
            module_name="numpy",
            alias="np"
        )
        self.assertEqual(import_info.effective_name, "np")

    def test_effective_name_without_alias(self):
        """Test effective_name property when no alias is provided."""
        # For global package import
        import_info1 = ImportInfo(
            import_type=ImportType.GLOBAL_PACKAGE,
            is_absolute=True,
            module_name="pandas"
        )
        self.assertEqual(import_info1.effective_name, "pandas")

        # For from import
        import_info2 = ImportInfo(
            import_type=ImportType.GLOBAL_FROM_PACKAGE,
            is_absolute=True,
            module_name="datetime",
            imported_object="datetime"
        )
        self.assertEqual(import_info2.effective_name, "datetime")

    def test_to_dict(self):
        """Test to_dict method."""
        import_info = ImportInfo(
            import_type=ImportType.GLOBAL_FROM_PACKAGE,
            is_absolute=True,
            module_name="json",
            imported_object="loads",
            alias="json_loads"
        )

        expected_dict = {
            "import_type": "global_from_package",
            "is_absolute": True,
            "module_name": "json",
            "imported_object": "loads",
            "alias": "json_loads",
            "relative_level": 0,
            "effective_name": "json_loads"
        }

        self.assertEqual(import_info.to_dict(), expected_dict)

    def test_str_representation(self):
        """Test string representation."""
        import_info = ImportInfo(
            import_type=ImportType.GLOBAL_PACKAGE,
            is_absolute=True,
            module_name="requests"
        )

        expected_str = "ImportInfo(type=global_package, absolute=True, module='requests', object=None, alias=None)"
        self.assertEqual(str(import_info), expected_str)

    def test_repr_representation(self):
        """Test repr representation."""
        import_info = ImportInfo(
            import_type=ImportType.GLOBAL_PACKAGE,
            is_absolute=True,
            module_name="requests"
        )

        expected_repr = "ImportInfo(type=global_package, absolute=True, module='requests', object=None, alias=None)"
        self.assertEqual(repr(import_info), expected_repr)


class TestImportInfoFromAST(unittest.TestCase):
    """Test cases for ImportInfo.from_ast method."""

    def test_from_ast_import_simple(self):
        """Test from_ast with simple import statement."""
        code = "import os"
        tree = ast.parse(code)
        import_node = tree.body[0]

        imports = ImportInfo.from_ast(import_node)
        self.assertEqual(len(imports), 1)

        import_info = imports[0]
        self.assertEqual(import_info.import_type, ImportType.GLOBAL_PACKAGE)
        self.assertTrue(import_info.is_absolute)
        self.assertEqual(import_info.module_name, "os")
        self.assertIsNone(import_info.imported_object)
        self.assertIsNone(import_info.alias)

    def test_from_ast_import_with_alias(self):
        """Test from_ast with import statement with alias."""
        code = "import numpy as np"
        tree = ast.parse(code)
        import_node = tree.body[0]

        imports = ImportInfo.from_ast(import_node)
        self.assertEqual(len(imports), 1)

        import_info = imports[0]
        self.assertEqual(import_info.import_type, ImportType.GLOBAL_PACKAGE)
        self.assertTrue(import_info.is_absolute)
        self.assertEqual(import_info.module_name, "numpy")
        self.assertEqual(import_info.alias, "np")

    def test_from_ast_import_relative(self):
        """Test from_ast with relative import statement."""
        code = "from . import utils"
        tree = ast.parse(code)
        import_node = tree.body[0]

        imports = ImportInfo.from_ast(import_node)
        self.assertEqual(len(imports), 1)

        import_info = imports[0]
        self.assertEqual(import_info.import_type,
                         ImportType.LOCAL_FROM_PACKAGE)
        self.assertFalse(import_info.is_absolute)
        self.assertEqual(import_info.module_name, "")
        self.assertEqual(import_info.imported_object, "utils")
        self.assertEqual(import_info.relative_level, 1)

    def test_from_ast_import_relative_multiple_dots(self):
        """Test from_ast with relative import statement with multiple dots."""
        code = "from .. import models"
        tree = ast.parse(code)
        import_node = tree.body[0]

        imports = ImportInfo.from_ast(import_node)
        self.assertEqual(len(imports), 1)

        import_info = imports[0]
        self.assertEqual(import_info.import_type,
                         ImportType.LOCAL_FROM_PACKAGE)
        self.assertFalse(import_info.is_absolute)
        self.assertEqual(import_info.module_name, "")
        self.assertEqual(import_info.imported_object, "models")
        self.assertEqual(import_info.relative_level, 2)

    def test_from_ast_import_from_simple(self):
        """Test from_ast with simple from import statement."""
        code = "from datetime import datetime"
        tree = ast.parse(code)
        import_node = tree.body[0]

        imports = ImportInfo.from_ast(import_node)
        self.assertEqual(len(imports), 1)

        import_info = imports[0]
        self.assertEqual(import_info.import_type,
                         ImportType.GLOBAL_FROM_PACKAGE)
        self.assertTrue(import_info.is_absolute)
        self.assertEqual(import_info.module_name, "datetime")
        self.assertEqual(import_info.imported_object, "datetime")

    def test_from_ast_import_from_with_alias(self):
        """Test from_ast with from import statement with alias."""
        code = "from json import loads as json_loads"
        tree = ast.parse(code)
        import_node = tree.body[0]

        imports = ImportInfo.from_ast(import_node)
        self.assertEqual(len(imports), 1)

        import_info = imports[0]
        self.assertEqual(import_info.import_type,
                         ImportType.GLOBAL_FROM_PACKAGE)
        self.assertTrue(import_info.is_absolute)
        self.assertEqual(import_info.module_name, "json")
        self.assertEqual(import_info.imported_object, "loads")
        self.assertEqual(import_info.alias, "json_loads")

    def test_from_ast_import_from_relative(self):
        """Test from_ast with relative from import statement."""
        code = "from .models import User"
        tree = ast.parse(code)
        import_node = tree.body[0]

        imports = ImportInfo.from_ast(import_node)
        self.assertEqual(len(imports), 1)

        import_info = imports[0]
        self.assertEqual(import_info.import_type,
                         ImportType.LOCAL_FROM_PACKAGE)
        self.assertFalse(import_info.is_absolute)
        self.assertEqual(import_info.module_name, "models")
        self.assertEqual(import_info.imported_object, "User")
        self.assertEqual(import_info.relative_level, 1)

    def test_from_ast_import_from_multiple_objects(self):
        """Test from_ast with from import statement with multiple objects."""
        code = "from os import path, makedirs"
        tree = ast.parse(code)
        import_node = tree.body[0]

        imports = ImportInfo.from_ast(import_node)
        self.assertEqual(len(imports), 2)

        # Check first import
        self.assertEqual(imports[0].import_type,
                         ImportType.GLOBAL_FROM_PACKAGE)
        self.assertEqual(imports[0].module_name, "os")
        self.assertEqual(imports[0].imported_object, "path")

        # Check second import
        self.assertEqual(imports[1].import_type,
                         ImportType.GLOBAL_FROM_PACKAGE)
        self.assertEqual(imports[1].module_name, "os")
        self.assertEqual(imports[1].imported_object, "makedirs")


class TestImportInfoFromString(unittest.TestCase):
    """Test cases for ImportInfo.from_string method."""

    def test_from_string_simple_import(self):
        """Test from_string with simple import statement."""
        code = "import os"
        imports = ImportInfo.from_string(code)

        self.assertEqual(len(imports), 1)
        self.assertEqual(imports[0].import_type, ImportType.GLOBAL_PACKAGE)
        self.assertEqual(imports[0].module_name, "os")

    def test_from_string_multiple_imports(self):
        """Test from_string with multiple import statements."""
        code = """
import os
import sys
from datetime import datetime
from . import helper
"""
        imports = ImportInfo.from_string(code)

        self.assertEqual(len(imports), 4)

        # Check import statements
        os_import = next(imp for imp in imports if imp.module_name == "os")
        self.assertEqual(os_import.import_type, ImportType.GLOBAL_PACKAGE)

        sys_import = next(imp for imp in imports if imp.module_name == "sys")
        self.assertEqual(sys_import.import_type, ImportType.GLOBAL_PACKAGE)

        # Check from import statements
        datetime_import = next(
            imp for imp in imports if imp.module_name == "datetime")
        self.assertEqual(datetime_import.import_type,
                         ImportType.GLOBAL_FROM_PACKAGE)

        helper_import = next(
            imp for imp in imports if imp.imported_object == "helper")
        self.assertEqual(helper_import.import_type,
                         ImportType.LOCAL_FROM_PACKAGE)

    def test_from_string_invalid_syntax(self):
        """Test from_string with invalid syntax."""
        code = "import os from"

        with self.assertRaises(ValueError):
            ImportInfo.from_string(code)

    def test_from_string_empty(self):
        """Test from_string with empty string."""
        imports = ImportInfo.from_string("")
        self.assertEqual(len(imports), 0)

    def test_from_string_no_imports(self):
        """Test from_string with code that has no imports."""
        code = "def hello(): print('Hello, World!')"
        imports = ImportInfo.from_string(code)
        self.assertEqual(len(imports), 0)


if __name__ == "__main__":
    unittest.main()
