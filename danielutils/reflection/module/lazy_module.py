"""
Lazy module loading functionality.

This module provides transparent lazy loading of optional modules,
allowing applications to start even when optional dependencies are missing.
The modules are only imported when actually used, providing clear error messages.
"""

import sys
from typing import Any, Optional


class LazyModule:
    """
    A proxy for modules that should only be imported when actually used.

    This allows code to run even when optional dependencies are missing,
    but provides clear error messages when the functionality is actually needed.
    """

    def __init__(self, module_name: str, error_message: str, install_hint: str):
        self._module_name = module_name
        self._module: Optional[Any] = None
        self._imported = False

        if not error_message:
            error_message = f"Module '{module_name}' is not available"

        if install_hint and install_hint.strip():
            error_message += f". {install_hint}"

        self._error_message = error_message

        # Set essential module attributes to make it look like a real module
        self.__name__ = module_name
        self.__file__ = None
        self.__package__ = None
        self.__path__ = None
        self.__spec__ = None

    def _ensure_imported(self):
        """Import the module if not already imported."""
        if not self._imported:
            # Check if there's already a real module in sys.modules
            existing_module = sys.modules.get(self._module_name)
            if existing_module is not self and existing_module is not None:
                # There's already a real module, use it
                self._module = existing_module
                self._imported = True
            else:
                # Try to import the real module
                try:
                    # Temporarily remove ourselves from sys.modules to avoid recursion
                    if existing_module is self:
                        del sys.modules[self._module_name]

                    self._module = __import__(self._module_name)
                    self._imported = True

                    # Restore ourselves to sys.modules
                    sys.modules[self._module_name] = self
                except ImportError:
                    # If import fails, raise the custom error message
                    raise ImportError(self._error_message)
        return self._module

    def __getattr__(self, name):
        """Delegate attribute access to the actual module."""
        # Try to import the module first
        try:
            module = self._ensure_imported()
            return getattr(module, name)
        except ImportError:
            # If import fails, raise the custom error message
            # This is runtime execution, not runtime loading
            raise ImportError(self._error_message)

    def __dir__(self):
        """Support dir() on the lazy module."""
        if self._imported:
            return dir(self._module)
        return []

    @property
    def module(self):
        """Access to the original module if it exists."""
        if self._imported and self._module is not None:
            return self._module
        return None

    def __repr__(self):
        if self._imported:
            return repr(self._module)
        return f"<LazyModule '{self._module_name}' (not imported)>"


def lazy_import(module_name: str, error_message: str, install_hint: str):
    """
    Set up lazy loading for a module.
    The module will be replaced in sys.modules with a LazyModule instance.
    It will only be truly imported when an attribute is accessed.
    """
    sys.modules[module_name] = LazyModule(
        module_name, error_message, install_hint)
