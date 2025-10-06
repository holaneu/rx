# **App Structure Redesign Specification**

## **Executive Summary**
This specification outlines the recommended restructuring of the app directory to improve maintainability, scalability, and code organization while preserving the simplified plugin loading system we recently implemented.

## **Current State Analysis**

### **Existing Structure (After Plugin Simplification)**
```
app/
├── configs/
│   ├── plugins_config.py         # NEW: Simplified plugin config
│   ├── app_config.py
│   ├── llm_config.py
│   └── module_config.py          # LEGACY: Complex, to be removed
├── utils/
│   ├── plugins_manager.py        # NEW: Simplified plugin loader
│   ├── registries.py            # Global registries
│   ├── module_manager.py         # LEGACY: Complex, to be removed
│   └── ...
├── prompts/
│   ├── __init__.py              # Core + plugin loading (3 lines)
│   └── _core.py                 # prompt() decorator, core functions
├── tools/
│   ├── __init__.py              # Core + plugin loading (3 lines)
│   └── _core.py                 # tool() decorator, core functions
└── workflows/
    ├── __init__.py              # Core + plugin loading (3 lines)
    └── _core.py                 # workflow() decorator, core functions
```

### **Current System Status**
- ✅ Plugin loading simplified and working (24 prompts, 23 workflows, 35 tools loaded)
- ✅ Single plugin location (plugins directory)
- ✅ Clean separation between core (app) and extensions (plugins)
- ❌ Management files scattered across `configs/` and `utils/`
- ❌ Legacy complex files still present

## **Recommended Target Structure**

### **Final Organization**
```
app/
├── core/                          # 🆕 Centralized management & shared functionality
│   ├── __init__.py               # Export commonly used items for clean imports
│   ├── plugins_manager.py        # Plugin loading logic (moved from utils/)
│   ├── plugins_config.py         # Plugin configuration (moved from configs/)
│   ├── registries.py             # Global registries (moved from utils/)
│   └── base.py                   # 🆕 Common base classes, shared decorators
├── prompts/                      # Prompt domain (unchanged structure)
│   ├── __init__.py               # Public API + plugin loading
│   └── _core.py                  # prompt() decorator, render_prompt_with_context()
├── tools/                        # Tool domain (unchanged structure)
│   ├── __init__.py               # Public API + plugin loading
│   └── _core.py                  # tool() decorator, tool-specific functions
├── workflows/                    # Workflow domain (unchanged structure)
│   ├── __init__.py               # Public API + plugin loading
│   └── _core.py                  # workflow() decorator, Workflow class
├── configs/                      # App-wide configuration only
│   ├── app_config.py            # Application settings (keep)
│   └── llm_config.py            # LLM configuration (keep)
└── utils/                        # General utilities (cleaned up)
    └── response_types.py         # Keep non-plugin utilities
```

### **Files to Remove/Archive**
```
❌ app/configs/module_config.py    # Legacy complex module config
❌ app/utils/module_manager.py     # Legacy complex module manager
```

## **Detailed Migration Plan**

### **Phase 1: Create Core Directory**
1. **Create** `app/core/` directory
2. **Create** __init__.py with common exports:
   ```python
   """Core functionality and management for the application."""
   
   from .plugins_manager import PluginsManager
   from .plugins_config import PluginsConfig
   from .registries import (
       PROMPTS_REGISTRY,
       WORKFLOWS_REGISTRY, 
       TOOLS_REGISTRY
   )
   
   __all__ = [
       'PluginsManager',
       'PluginsConfig', 
       'PROMPTS_REGISTRY',
       'WORKFLOWS_REGISTRY',
       'TOOLS_REGISTRY'
   ]
   ```

### **Phase 2: Move Management Files**
1. **Move** plugins_manager.py → `app/core/plugins_manager.py`
2. **Move** plugins_config.py → `app/core/plugins_config.py`
3. **Move** registries.py → registries.py

### **Phase 3: Update Import Statements**
**In Package __init__.py Files:**
```python
# OLD (current):
from app.utils.plugins_manager import PluginsManager

# NEW (target):
from app.core import PluginsManager
```

**Update these files:**
- __init__.py
- __init__.py  
- __init__.py

### **Phase 4: Create Base Module**
**Create** `app/core/base.py` for shared functionality:
```python
"""Base classes and common functionality shared across domains."""

# Future: Common base classes, shared decorators, utility functions
# that are used across prompts, tools, and workflows
```

### **Phase 5: Clean Legacy Files**
1. **Remove** module_config.py
2. **Remove** module_manager.py
3. **Clean up** any remaining references to old system

## **Benefits of This Structure**

### **🎯 Clear Separation of Concerns**
- **`app/core/`**: Shared management, plugin loading, registries
- **prompts**: Prompt-specific functionality and API
- **tools**: Tool-specific functionality and API  
- **workflows**: Workflow-specific functionality and API
- **configs**: Application-wide configuration only

### **⚡ Clean Import Patterns**
```python
# Public APIs (unchanged - backward compatible)
from app.prompts import prompt, render_prompt_with_context
from app.workflows import workflow, Workflow
from app.tools import tool

# Core functionality (improved)
from app.core import PluginsManager, PROMPTS_REGISTRY

# vs old scattered imports:
from app.utils.plugins_manager import PluginsManager
from app.configs.plugins_config import PluginsConfig
```

### **📈 Scalability & Maintainability**
- **Logical Grouping**: Related files together
- **Easy Discovery**: Developers know where to find functionality
- **Future-Proof**: Easy to extend without major restructuring
- **Domain Boundaries**: Clear ownership of functionality

### **🛡️ Backward Compatibility**
- **Public APIs unchanged**: No breaking changes for users
- **Plugin system intact**: All current plugins continue working
- **Gradual migration**: Can be done incrementally

## **Implementation Guidelines**

### **File Naming Conventions**
- **Core files**: Descriptive names (`plugins_manager.py`, `plugins_config.py`)
- **Domain files**: Keep current naming (`_core.py` for implementation)
- **Package files**: Standard __init__.py for public APIs

### **Import Strategy**
- **Internal imports**: Use relative imports within domains
- **Cross-domain imports**: Use absolute imports through `app.core`
- **Public APIs**: Export through package __init__.py files

### **Testing Strategy**
- **Verify plugin loading**: All current plugins still load correctly
- **Test import paths**: Both old and new import paths work during migration
- **Validate functionality**: All decorators and registries function properly

## **Success Criteria**

### **Functional Requirements**
- ✅ All plugins load correctly (24 prompts, 23 workflows, 35 tools)
- ✅ All decorators work (`@prompt`, `@workflow`, `@tool`)
- ✅ Public APIs remain unchanged
- ✅ Plugin hot-reloading continues to work

### **Structural Requirements**
- ✅ Clear separation between core management and domain logic
- ✅ Logical file organization in `app/core/`
- ✅ Clean import patterns established
- ✅ Legacy files removed

### **Quality Requirements**
- ✅ No regression in performance
- ✅ Improved code discoverability
- ✅ Better maintainability
- ✅ Clear documentation and examples

## **Risk Assessment**

### **Low Risk**
- **File moves**: Simple file relocations with import updates
- **New directory**: Adding `app/core/` is non-breaking

### **Mitigation Strategies**
- **Incremental approach**: Move one file at a time
- **Test after each step**: Verify functionality continues working
- **Backup branch**: Keep current working state as fallback

This specification provides a clear roadmap for creating a well-organized, maintainable application structure while preserving all current functionality and the simplified plugin system we've successfully implemented.