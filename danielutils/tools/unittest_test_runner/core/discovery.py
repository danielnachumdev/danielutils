"""
Test discovery and structure analysis functionality.
"""

import logging
import os
import subprocess
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Literal
from ..models import TestDiscovery

logger = logging.getLogger(__name__)

VerboseLevel = Literal["module", "file", "class", "function"]


class TestDiscoveryService:
    """Handles discovery of test structure and target parsing."""
    
    def __init__(self, python_path: str, verbose: VerboseLevel = "class"):
        logger.debug("Initializing TestDiscoveryService with python_path=%s, verbose=%s", python_path, verbose)
        self._python_path = python_path
        self._verbose = verbose
    
    def discover_test_modules(self, tests_dir: str = "tests", target: Optional[str] = None) -> List[str]:
        """Discover all test modules based on target or default tests directory."""
        logger.info("Discovering test modules with tests_dir=%s, target=%s", tests_dir, target)
        
        if target:
            # If specific target provided, look for tests relative to that target
            logger.debug("Target specified, looking for modules matching: %s", target)
            if "." in target:
                # Target is a module path, look for tests in that module's directory
                target_parts = target.split(".")
                if target_parts[0] == "test_runner":
                    # Look in test_runner/tests directory
                    tests_path = Path("test_runner/tests")
                else:
                    # Look in the main tests directory
                    tests_path = Path("tests")
            else:
                # Single module name, look in default tests directory
                tests_path = Path("tests")
            
            if tests_path.exists():
                found_modules = []
                logger.debug("Searching for test files in: %s", tests_path)
                for py_file in tests_path.rglob("test_*.py"):
                    # Convert path to module format
                    relative_path = py_file.relative_to(tests_path.parent)
                    module_path = str(relative_path).replace(os.sep, ".").replace(".py", "")
                    # Check if this module matches our target
                    if module_path.startswith(target):
                        found_modules.append(module_path)
                        logger.debug("Found matching module: %s", module_path)
                
                # If we're looking for a specific module.class target, find all test modules in that module
                if "." in target and not found_modules:
                    # Split target like "test_runner.tests" into "test_runner" and "tests"
                    target_parts = target.split(".")
                    if len(target_parts) >= 2:
                        module_prefix = ".".join(target_parts[:-1])  # "test_runner" for "test_runner.tests"
                        logger.debug("No exact matches, trying module prefix: %s", module_prefix)
                        for py_file in tests_path.rglob("test_*.py"):
                            relative_path = py_file.relative_to(tests_path.parent)
                            module_path = str(relative_path).replace(os.sep, ".").replace(".py", "")
                            if module_path.startswith(module_prefix):
                                found_modules.append(module_path)
                                logger.debug("Found module with prefix match: %s", module_path)
                
                if found_modules:
                    logger.info("Discovered %d test modules for target '%s'", len(found_modules), target)
                    if self._verbose in ["module", "file", "class", "function"]:
                        print(f"  📁 Discovered {len(found_modules)} test module(s) for target '{target}':")
                        for module in sorted(found_modules):
                            print(f"    📄 {module}")
                    return found_modules
            
            # If no tests found relative to target, return the target itself
            logger.warning("No test modules found for target '%s', using target as module", target)
            if self._verbose in ["module", "file", "class", "function"]:
                print(f"  📁 No test modules found for target '{target}', using target as module")
            return [target]
        
        # No target provided, look in the default tests directory
        test_modules = []
        tests_path = Path(tests_dir)
        
        if not tests_path.exists():
            logger.error("Tests directory not found: %s", tests_dir)
            print(f"Tests directory not found: {tests_dir}")
            return []
        
        logger.debug("Searching for test files in default directory: %s", tests_path)
        for py_file in tests_path.rglob("test_*.py"):
            # Convert path to module format
            relative_path = py_file.relative_to(tests_path.parent)
            module_path = str(relative_path).replace(os.sep, ".").replace(".py", "")
            test_modules.append(module_path)
            logger.debug("Found test module: %s", module_path)
        
        logger.info("Discovered %d test modules in '%s'", len(test_modules), tests_dir)
        if self._verbose in ["module", "file", "class", "function"]:
            print(f"  📁 Discovered {len(test_modules)} test module(s) in '{tests_dir}':")
            for module in sorted(test_modules):
                print(f"    📄 {module}")
            
        return sorted(test_modules)
    
    def discover_test_structure(self, test_modules: List[str]) -> TestDiscovery:
        """Discover the complete test structure for progress tracking."""
        logger.info("Discovering test structure for %d modules", len(test_modules))
        if self._verbose in ["module", "file", "class", "function"]:
            print(f"  🔍 Discovering test structure for {len(test_modules)} module(s)...")
        
        modules = []
        classes = {}  # module -> list of classes
        functions = {}  # class -> list of functions
        total_functions = 0
        total_classes = 0
        
        for i, module_path in enumerate(test_modules):
            modules.append(module_path)
            
            logger.debug("Analyzing module %d/%d: %s", i+1, len(test_modules), module_path)
            if self._verbose in ["class", "function"]:
                print(f"    📦 Analyzing module {i+1}/{len(test_modules)}: {module_path}")
            
            # Discover classes and functions in this module
            try:
                # Run unittest discovery to get test structure
                cmd = [self._python_path, "-m", "unittest", "discover", "-s", "tests", "-p", f"{module_path.split('.')[-1]}.py", "--dry-run"]
                logger.debug("Running discovery command: %s", " ".join(cmd))
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                
                if result.returncode == 0:
                    logger.debug("Discovery command successful for module: %s", module_path)
                    # Parse the discovery output to find classes and functions
                    module_classes = []
                    for line in result.stdout.split('\n'):
                        if 'test_' in line and '(' in line and ')' in line:
                            # Extract class name from line like "test_something (class_name)"
                            parts = line.split()
                            for part in parts:
                                if part.startswith('(') and part.endswith(')'):
                                    class_name = part[1:-1]
                                    if class_name not in module_classes:
                                        module_classes.append(class_name)
                                        
                                        # Count functions for this class
                                        class_functions = []
                                        for func_line in result.stdout.split('\n'):
                                            if f'({class_name})' in func_line and 'test_' in func_line:
                                                func_parts = func_line.split()
                                                for func_part in func_parts:
                                                    if func_part.startswith('test_'):
                                                        class_functions.append(func_part)
                                                        break
                                        
                                        functions[f"{module_path}.{class_name}"] = class_functions
                                        total_functions += len(class_functions)
                                        logger.debug("Found class %s with %d functions", class_name, len(class_functions))
                    
                    classes[module_path] = module_classes
                    total_classes += len(module_classes)
                    
                    if self._verbose == "function":
                        if module_classes:
                            print(f"      🏛️  Found {len(module_classes)} test class(es): {', '.join(module_classes)}")
                            for class_name in module_classes:
                                class_funcs = functions.get(f"{module_path}.{class_name}", [])
                                if class_funcs:
                                    print(f"        🧪 {class_name}: {len(class_funcs)} function(s) - {', '.join(class_funcs[:3])}{'...' if len(class_funcs) > 3 else ''}")
                        else:
                            print(f"      ⚠️  No test classes found")
                else:
                    logger.warning("Discovery command failed for module %s (returncode: %d)", module_path, result.returncode)
                    # Fallback: assume one class per module
                    classes[module_path] = ["UnknownClass"]
                    functions[f"{module_path}.UnknownClass"] = []
                    
            except Exception as e:
                logger.error("Error discovering structure for module %s: %s", module_path, e)
                if self._verbose in ["class", "function"]:
                    print(f"      ❌ Error discovering structure for {module_path}: {e}")
                # Fallback: assume one class per module
                classes[module_path] = ["UnknownClass"]
                functions[f"{module_path}.UnknownClass"] = []
        
        logger.info("Test structure discovery complete: %d modules, %d classes, %d functions", 
                   len(modules), total_classes, total_functions)
        if self._verbose in ["module", "file", "class", "function"]:
            print(f"  ✅ Discovery complete: {len(modules)} modules, {total_classes} classes, {total_functions} functions")
        
        discovery = TestDiscovery(
            modules=modules,
            classes=classes,
            functions=functions,
            total_functions=total_functions,
            total_classes=total_classes,
            total_modules=len(modules)
        )
        
        if self._verbose == "function":
            print(f"DEBUG: Discovered {len(modules)} modules, {total_classes} classes, {total_functions} functions")
        
        return discovery
    
    def parse_target(self, target: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        """Parse unittest dot-notation target into module, class, function components."""
        logger.debug("Parsing target: %s", target)
        if not target:
            return None, None, None
        
        parts = target.split('.')
        
        # Handle different cases:
        # 1. "module" -> module=module, class=None, function=None
        # 2. "module.class" -> module=module, class=class, function=None  
        # 3. "module.class.function" -> module=module, class=class, function=function
        # 4. "module.class.function.too.much" -> module=module.class.function, class=too, function=much
        
        if len(parts) == 1:
            # Just module name
            module = parts[0]
            class_name = None
            function_name = None
        elif len(parts) == 2:
            # Could be module.class or module.submodule
            # Check if second part starts with uppercase (class) or lowercase (submodule)
            if parts[1][0].isupper():
                # Second part starts with uppercase, it's a class
                module = parts[0]
                class_name = parts[1]
                function_name = None
            else:
                # Second part starts with lowercase, it's a submodule
                module = '.'.join(parts)
                class_name = None
                function_name = None
        elif len(parts) == 3:
            # Module.submodule.class - join first two as module, third is class
            module = '.'.join(parts[:2])
            class_name = parts[2]
            function_name = None
        else:
            # More than 3 parts - for invalid formats like "invalid.target.too.many.parts"
            # Join first 2 parts as module, take 3rd as class, last part as function
            module = '.'.join(parts[:2])
            class_name = parts[2]
            function_name = parts[-1]
        
        logger.debug("Parsed target components - module: %s, class: %s, function: %s", module, class_name, function_name)
        return module, class_name, function_name
    
    def create_focused_discovery(self, target_module: str, target_class: Optional[str], 
                               target_function: Optional[str], full_discovery: TestDiscovery) -> TestDiscovery:
        """Create a focused test discovery based on target specification."""
        logger.debug("Creating focused discovery for target: %s.%s.%s", target_module, target_class or '', target_function or '')
        if self._verbose == "function":
            print(f"DEBUG: Creating focused discovery for target: {target_module}.{target_class or ''}.{target_function or ''}")
        
        # Find the target module
        target_modules = [m for m in full_discovery.modules if m == target_module or m.endswith(f".{target_module}")]
        if not target_modules:
            logger.error("Target module '%s' not found in discovered modules", target_module)
            raise ValueError(f"Target module '{target_module}' not found in discovered modules")
        
        module = target_modules[0]
        modules = [module]
        classes = {}
        functions = {}
        
        # Get classes for this module
        module_classes = full_discovery.classes.get(module, [])
        logger.debug("Found %d classes in target module %s", len(module_classes), module)
        
        if target_class:
            # Filter to specific class
            if target_class in module_classes:
                logger.debug("Filtering to specific class: %s", target_class)
                classes[module] = [target_class]
                class_key = f"{module}.{target_class}"
                class_functions = full_discovery.functions.get(class_key, [])
                
                if target_function:
                    # Filter to specific function
                    if target_function in class_functions:
                        logger.debug("Filtering to specific function: %s", target_function)
                        functions[class_key] = [target_function]
                    else:
                        logger.warning("Target function '%s' not found in class '%s'", target_function, target_class)
                        functions[class_key] = []
                else:
                    functions[class_key] = class_functions
                    logger.debug("Including all %d functions in class %s", len(class_functions), target_class)
            else:
                logger.warning("Target class '%s' not found in module '%s'", target_class, module)
                classes[module] = []
                functions[f"{module}.{target_class}"] = []
        else:
            # Include all classes in module
            logger.debug("Including all %d classes in module %s", len(module_classes), module)
            classes[module] = module_classes
            for class_name in module_classes:
                class_key = f"{module}.{class_name}"
                functions[class_key] = full_discovery.functions.get(class_key, [])
        
        total_functions = sum(len(funcs) for funcs in functions.values())
        total_classes = sum(len(cls) for cls in classes.values())
        
        logger.info("Created focused discovery: %d modules, %d classes, %d functions", 
                   len(modules), total_classes, total_functions)
        
        return TestDiscovery(
            modules=modules,
            classes=classes,
            functions=functions,
            total_functions=total_functions,
            total_classes=total_classes,
            total_modules=len(modules)
        )
