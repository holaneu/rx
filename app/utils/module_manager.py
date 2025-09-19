import os
import sys
import ast
import re
import importlib
import importlib.util
from pathlib import Path
from typing import Dict, List, Optional, Union
from app.configs.module_config import ModuleConfig, ModuleCategories, PackageTypes
from app.configs.app_config import APP_SETTINGS

class ModuleManager:
    """Unified module management for both static imports and dynamic registry loading."""
    
    def __init__(self):
        self.AUTO_START = "# AUTO-GENERATED-IMPORTS-START"
        self.AUTO_END = "# AUTO-GENERATED-IMPORTS-END"
        self.config = ModuleConfig()
        self.ignore_modules = {"__init__.py", "core.py", "_core.py"}
    
    def full_reload(self, categories: Optional[List[str]] = None, package_types: Optional[List[str]] = None):
        """
        Complete reload: static imports + registry updates.
        
        Args:
            categories: ["app", "admin", "extensions", "user_custom"] or None for all
            package_types: ["workflows", "assistants", "tools", "prompts"] or None for all
        """
        if not categories:
            categories = [category.value for category in ModuleCategories]
        if not package_types:
            package_types = [package.value for package in PackageTypes]
        
        # 1. Update static imports for each category
        for category in categories:
            self._update_static_imports_for_category(category)
        
        # 2. Reload dynamic modules for each package type
        for package_type in package_types:
            registry = self.config.get_registry_for_package(package_type)
            if registry is not None:
                self._load_dynamic_modules_for_package(package_type, registry)
        
        # 3. Invalidate Python import cache
        importlib.invalidate_caches()
    
    def _update_static_imports_for_category(self, category: str):
        """Update __init__.py files for all packages in a category."""
        category_paths = self.config.get_category_paths(category)
        
        for directory in category_paths:
            directory_path = Path(directory)
            if directory_path.exists():
                init_path = directory_path / "__init__.py"
                existing_symbols = self._get_existing_symbols(init_path)
                new_auto_block = self._generate_imports(directory_path, existing_symbols)
                self._update_init_file(init_path, new_auto_block)
                
                # Reload the Python module
                try:
                    pkg_name = str(directory_path).replace("/", ".").replace("\\", ".")
                    if pkg_name in sys.modules:
                        importlib.reload(sys.modules[pkg_name])
                except Exception:
                    pass  # Silently continue if reload fails
    
    def _load_dynamic_modules_for_package(self, package_type: str, registry: Dict[str, dict]):
        """Load user custom modules into registry for a specific package type."""
        # Only load from user_custom directory for dynamic loading
        user_custom_paths = self.config.get_all_module_paths().get(ModuleCategories.USER.value, {})
        directory = user_custom_paths.get(package_type)
        
        directory_path = Path(directory) if directory else None
        if not directory_path or not directory_path.is_dir():
            return
        
        # Clean existing user modules from registry
        module_prefix = "user." + package_type  # Use simplified prefix
        keys_to_remove = [
            key for key, value in registry.items()
            if isinstance(value, dict) and value.get("module", "").startswith(module_prefix)
        ]
        for key in keys_to_remove:
            del registry[key]
        
        # Remove from sys.modules
        for module_name in list(sys.modules):
            if module_name.startswith(module_prefix):
                del sys.modules[module_name]
        
        # Load new modules using simple import method
        self._load_modules_from_directory_simple(directory_path, package_type)
    
    def _ensure_parent_packages(self, mod_name: str):
        """Ensure all parent packages exist in sys.modules."""
        parts = mod_name.split('.')
        for i in range(len(parts) - 1):  # Exclude the module itself, only do parents
            parent_name = '.'.join(parts[:i+1])
            if parent_name not in sys.modules:
                # Try to import the actual package first
                try:
                    parent_module = importlib.import_module(parent_name)
                    sys.modules[parent_name] = parent_module
                except ImportError:
                    # If import fails, create a minimal module
                    parent_module = importlib.util.module_from_spec(
                        importlib.util.spec_from_loader(parent_name, loader=None)
                    )
                    sys.modules[parent_name] = parent_module

    def _load_modules_from_directory_simple(self, directory_path: Path, package_type: str):
        """Load all Python modules from a directory using simple Python imports."""
        # Ensure paths are in sys.path
        app_root = Path(__file__).parent.parent.parent
        user_path = app_root / "user"
        
        if str(app_root) not in sys.path:
            sys.path.insert(0, str(app_root))
        if str(user_path) not in sys.path:
            sys.path.insert(0, str(user_path))
        
        # Import all Python files in the directory
        for py_file in directory_path.glob("*.py"):
            if py_file.name not in {"__init__.py", "_core.py", "core.py"}:
                try:
                    module_name = f"user.{package_type}.{py_file.stem}"
                    # Remove from sys.modules if already imported to force fresh import
                    if module_name in sys.modules:
                        del sys.modules[module_name]
                    
                    # Use exec with dynamic import - this is what worked in debug/simple_test
                    exec(f"from user.{package_type} import {py_file.stem}")
                    
                except Exception:
                    # Continue with other modules if one fails
                    pass

    def _load_modules_from_directory(self, directory: Union[str, Path], package_type: str):
        """DEPRECATED: Load all Python modules from a directory using complex importlib method."""
        # This method is kept for backwards compatibility but not used
        # The simple method above is used instead
        pass
    
    # Helper methods from original update_init2.py
    def _extract_symbols(self, filepath: Union[str, Path]):
        filepath = Path(filepath)
        with filepath.open("r", encoding="utf-8") as f:
            node = ast.parse(f.read(), str(filepath))
        symbols = []
        for n in node.body:
            if isinstance(n, ast.FunctionDef):
                symbols.append(n.name)
            elif isinstance(n, ast.ClassDef):
                symbols.append(n.name)
        return symbols

    def _get_existing_symbols(self, init_path: Union[str, Path]):
        init_path = Path(init_path)
        if not init_path.exists():
            return set()
        with init_path.open("r", encoding="utf-8") as f:
            content = f.read()
        pattern = re.compile(f"{self.AUTO_START}.*?{self.AUTO_END}", re.DOTALL)
        content_no_auto = pattern.sub("", content)
        match = re.search(r"__all__\s*=\s*\[([^\]]*)\]", content_no_auto)
        if not match:
            return set()
        items = re.findall(r'"([^"]+)"', match.group(1))
        return set(items)

    def _generate_imports(self, directory: Union[str, Path], existing_symbols):
        directory_path = Path(directory)
        import_lines = []
        all_names = []
        
        for file_path in sorted(directory_path.rglob("*.py")):
            if file_path.name not in ["__init__.py", "core.py", "_core.py"]:
                symbols = self._extract_symbols(file_path)
                symbols = [s for s in symbols if not s.startswith("_") and s not in existing_symbols]
                if symbols:
                    rel_path = file_path.relative_to(directory_path)
                    parts = rel_path.with_suffix('').parts
                    import_path = ".".join(parts)
                    import_lines.append(f"from .{import_path} import {', '.join(symbols)}")
                    all_names.extend(symbols)
        
        if not all_names:
            return ""
        imports_block = "\n".join(import_lines)
        all_block = "__all__ = [\n    " + ",\n    ".join(f'"{name}"' for name in all_names) + ",\n]"
        return imports_block + "\n\n" + all_block

    def _update_init_file(self, init_path: Union[str, Path], new_auto_block):
        init_path = Path(init_path)
        if not init_path.exists():
            with init_path.open("w", encoding="utf-8") as f:
                f.write(f"{self.AUTO_START}\n{self.AUTO_END}\n")
        
        with init_path.open("r", encoding="utf-8") as f:
            content = f.read()
        
        pattern = re.compile(f"{self.AUTO_START}.*?{self.AUTO_END}", re.DOTALL)
        if new_auto_block.strip():
            replacement = f"{self.AUTO_START}\n{new_auto_block}\n{self.AUTO_END}"
        else:
            replacement = f"{self.AUTO_START}\n{self.AUTO_END}"
        
        if pattern.search(content):
            content = pattern.sub(replacement, content)
        else:
            content = f"{replacement}\n\n" + content
        
        with init_path.open("w", encoding="utf-8") as f:
            f.write(content)