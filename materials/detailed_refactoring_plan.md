# **Detailní Plán Refaktoringu App Struktury RX**

## **Executive Summary**
Tento dokument obsahuje detailní plán refaktoringu aplikační struktury podle specifikace `app_structure_redesign.md`, včetně rozšíření o Flask blueprints pro API, UI a files management. Plán zachovává plnou funkčnost během migrace a respektuje Python coding instructions.

## **Aktuální Analýza Codebase**

### **Současný Stav (Po Analýze)**
```
app/
├── configs/
│   ├── plugins_config.py         ✅ Funkční, čistý kód
│   ├── app_config.py            ✅ Zachovat
│   └── llm_config.py            ✅ Zachovat
├── utils/
│   ├── plugins_manager.py        ✅ Funkční, přesunout
│   ├── registries.py            ✅ Funkční, přesunout
│   └── response_types.py         ✅ Zachovat v utils/
├── prompts/
│   ├── __init__.py              ✅ Aktualizovat import
│   └── _core.py                 ✅ Zachovat
├── tools/
│   ├── __init__.py              ✅ Aktualizovat import
│   └── _core.py                 ✅ Zachovat
├── workflows/
│   ├── __init__.py              ✅ Aktualizovat import
│   └── _core.py                 ✅ Zachovat
├── ui/                          🆕 Rozšířit o blueprint
│   ├── static/                  ✅ Zachovat
│   └── templates/               ✅ Zachovat
└── storage/                     🆕 Rozšířit o blueprint
    ├── manager.py               ✅ Zachovat
    └── models.py                ✅ Zachovat
```

### **Klíčové Pozorování**
1. **Legacy soubory již neexistují**: `module_config.py` a `module_manager.py` již nejsou v codebase
2. **Plugin systém funguje**: 24 prompts, 23 workflows, 35 tools se úspěšně načítají
3. **Čisté importy**: Všechny importy používají správné cesty podle Python instructions
4. **Flask routes v main.py**: Potřeba rozdělit do blueprints

## **Cílová Struktura s Blueprints**

### **Finální Organizace**
```
app/
├── core/                        🆕 Centralizované řízení
│   ├── __init__.py             # Čisté exporty
│   ├── plugins_manager.py      # Přesun z utils/
│   ├── plugins_config.py       # Přesun z configs/
│   ├── registries.py           # Přesun z utils/
│   └── base.py                 # Sdílené třídy
├── blueprints/                  🆕 Flask blueprints
│   ├── __init__.py             # Registrace blueprints
│   ├── api.py                  # API routes (/api/*)
│   ├── ui.py                   # UI routes (/, /workflows)
│   └── files.py                # Files routes (/files/*)
├── prompts/                     # Nezměněno
│   ├── __init__.py             # Aktualizovaný import
│   └── _core.py                # Nezměněno
├── tools/                       # Nezměněno
│   ├── __init__.py             # Aktualizovaný import
│   └── _core.py                # Nezměněno
├── workflows/                   # Nezměněno
│   ├── __init__.py             # Aktualizovaný import
│   └── _core.py                # Nezměněno
├── configs/                     # Pouze app-wide konfigurace
│   ├── app_config.py           # Nezměněno
│   └── llm_config.py           # Nezměněno
├── utils/                       # Obecné utility
│   └── response_types.py       # Nezměněno
├── ui/                         # UI resources
│   ├── static/                 # Nezměněno
│   └── templates/              # Nezměněno
└── storage/                    # Data management
    ├── manager.py              # Nezměněno
    └── models.py               # Nezměněno
```

## **Detailní Migrační Plán**

### **FÁZE 1: Vytvoření Core Directory**
**Cíl**: Centralizovat management funkcionalitu

**Kroky**:
1. Vytvořit `app/core/` directory
2. Vytvořit `app/core/__init__.py` s exporty:
```python
"""Core functionality and management for the application."""

from .plugins_manager import PluginsManager
from .plugins_config import PluginsConfig
from .registries import (
    PROMPTS_REGISTRY,
    WORKFLOWS_REGISTRY, 
    TOOLS_REGISTRY,
    ASSISTANTS_REGISTRY
)

__all__ = [
    'PluginsManager',
    'PluginsConfig', 
    'PROMPTS_REGISTRY',
    'WORKFLOWS_REGISTRY',
    'TOOLS_REGISTRY',
    'ASSISTANTS_REGISTRY'
]
```

3. Vytvořit `app/core/base.py` pro sdílenou funkcionalitat:
```python
"""Base classes and common functionality shared across domains."""

from pathlib import Path


class BaseManager:
    """Base class for all managers with common utility methods."""
    
    @staticmethod
    def get_project_root() -> Path:
        """Get project root directory using absolute path resolution."""
        # Use Path(__file__).resolve().parent to ensure compatibility with PythonAnywhere
        current_file_path = Path(__file__).resolve()
        
        # Walk up the directory tree to find project root (contains both 'app' and 'plugins')
        for parent_path in current_file_path.parents:
            if (parent_path / "app").exists() and (parent_path / "plugins").exists():
                return parent_path
        
        raise Exception("Could not find project root directory containing both 'app' and 'plugins' folders")


class BaseConfig:
    """Base configuration class with path resolution utilities."""
    
    @classmethod
    def resolve_absolute_path(cls, relative_path: str) -> Path:
        """Resolve relative path to absolute path from project root."""
        project_root = BaseManager.get_project_root()
        return project_root / relative_path
```

### **FÁZE 2: Přesun Management Files**
**Cíl**: Konsolidovat management logiku

**Kroky**:
1. **Přesunout** `app/utils/plugins_manager.py` → `app/core/plugins_manager.py`
   - Aktualizovat import: `from app.configs.plugins_config import PluginsConfig` → `from .plugins_config import PluginsConfig`

2. **Přesunout** `app/configs/plugins_config.py` → `app/core/plugins_config.py`
   - Aktualizovat import: `from app.utils.registries import (...)` → `from .registries import (...)`
   - Aktualizovat path resolution podle Python instructions:
   ```python
   # SOUČASNÝ (relativní path):
   PLUGINS_ROOT = Path(__file__).resolve().parent.parent.parent / "plugins"
   
   # NOVÝ (použití base class):
   from .base import BaseConfig
   PLUGINS_ROOT = BaseConfig.resolve_absolute_path("plugins")
   ```

3. **Přesunout** `app/utils/registries.py` → `app/core/registries.py`
   - Žádné změny v obsahu

### **FÁZE 3: Vytvoření Flask Blueprints**
**Cíl**: Rozdělit monolitický main.py do modulárních blueprints

**3.1 Vytvořit Blueprint Infrastructure**

1. **Vytvořit** `app/blueprints/__init__.py`:
```python
"""Flask blueprints for modular route organization."""

from flask import Flask
from .api import api_blueprint
from .ui import ui_blueprint
from .files import files_blueprint


def register_blueprints(flask_app: Flask) -> None:
    """Register all application blueprints with the Flask app."""
    
    # Register API blueprint with '/api' prefix
    flask_app.register_blueprint(api_blueprint, url_prefix='/api')
    
    # Register UI blueprint (no prefix for root routes)
    flask_app.register_blueprint(ui_blueprint)
    
    # Register files blueprint with '/files' prefix  
    flask_app.register_blueprint(files_blueprint, url_prefix='/files')


__all__ = [
    'register_blueprints',
    'api_blueprint',
    'ui_blueprint', 
    'files_blueprint'
]
```

**3.2 API Blueprint** (`app/blueprints/api.py`):
```python
"""API routes blueprint for handling all /api/* endpoints."""

from flask import Blueprint, request, jsonify
import uuid
import inspect

# Import from new core location
from app.core import WORKFLOWS_REGISTRY, PROMPTS_REGISTRY, TOOLS_REGISTRY
from app.core import PluginsManager
from app.utils.response_types import response_output_error, ResponseKey, ResponseStatus

api_blueprint = Blueprint('api', __name__)


@api_blueprint.route('/start_task', methods=['POST'])
def start_task():
    """Start workflow execution task."""
    # Přesunout logiku z main.py
    pass


@api_blueprint.route('/continue_task', methods=['POST'])  
def continue_task():
    """Continue workflow execution task."""
    # Přesunout logiku z main.py
    pass


@api_blueprint.route('/tools/test', methods=['POST'])
def test_tools():
    """Test tool execution."""
    # Přesunout logiku z main.py
    pass


@api_blueprint.route('/diagnostic', methods=['GET'])
def diagnostic():
    """System diagnostic information."""
    # Přesunout logiku z main.py
    pass


@api_blueprint.route('/reload_plugins', methods=['GET', 'POST'])
def reload_plugins():
    """Reload all plugins."""
    # Přesunout logiku z main.py
    pass
```

**3.3 UI Blueprint** (`app/blueprints/ui.py`):
```python
"""UI routes blueprint for rendering web pages."""

from flask import Blueprint, render_template
from app.core import WORKFLOWS_REGISTRY
from app.configs.llm_config import llm_models

ui_blueprint = Blueprint('ui', __name__)


def get_workflows_catalog():
    """Return workflows registry for template rendering."""
    # Přesunout z main.py s aktualizovanými importy
    pass


@ui_blueprint.route('/')
def index():
    """Main page."""
    # Přesunout logiku z main.py
    pass


@ui_blueprint.route('/workflows')
def workflows():
    """Workflows page."""  
    # Přesunout logiku z main.py
    pass
```

**3.4 Files Blueprint** (`app/blueprints/files.py`):
```python
"""Files management routes blueprint."""

from flask import Blueprint, render_template, abort, redirect, url_for
from app.storage.manager import FileStorageManager

files_blueprint = Blueprint('files', __name__)

# Initialize file manager
file_manager = FileStorageManager()


@files_blueprint.route('/')
def files_redirect():
    """Handle trailing slash redirect."""
    # Přesunout logiku z main.py
    pass


@files_blueprint.route('')
@files_blueprint.route('/folder/<item_id>')
def files(item_id=None):
    """Files browser."""
    # Přesunout logiku z main.py
    pass


@files_blueprint.route('/file/<item_id>')
def file_detail(item_id):
    """File detail view."""
    # Přesunout logiku z main.py
    pass
```

### **FÁZE 4: Aktualizace Import Statements**
**Cíl**: Aktualizovat všechny importy na nové cesty

**4.1 Domain Packages** (`app/prompts/__init__.py`, `app/tools/__init__.py`, `app/workflows/__init__.py`):
```python
# SOUČASNÝ:
from app.utils.plugins_manager import PluginsManager

# NOVÝ:
from app.core import PluginsManager
```

**4.2 Main Application** (`main.py`):
```python
# SOUČASNÝ:
from app.utils.registries import WORKFLOWS_REGISTRY
from app.utils.plugins_manager import PluginsManager

# NOVÝ:
from app.core import WORKFLOWS_REGISTRY, PluginsManager
from app.blueprints import register_blueprints

# Aktualizace Flask app setup:
app = Flask(__name__, static_folder='app/ui/static', template_folder='app/ui/templates')

# Registrace blueprints místo inline routes
register_blueprints(app)
```

### **FÁZE 5: Refaktoring Main.py**
**Cíl**: Zjednodušit main.py na core aplikační logiku

**Nový main.py struktura**:
```python
"""Main application entry point with Flask setup and blueprint registration."""

from flask import Flask
from flask_cors import CORS
from pathlib import Path
from dotenv import load_dotenv
import os

# Import core functionality
from app.core import PluginsManager
from app.blueprints import register_blueprints
from app.configs.app_config import APP_SETTINGS

# ----------------------
# Flask app setup
app = Flask(__name__, static_folder='app/ui/static', template_folder='app/ui/templates')

# Enable CORS for API routes only
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Setup environment
dotenv_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path)

# Register all blueprints
register_blueprints(app)

# ----------------------
# Plugin loading
def load_plugins_at_startup():
    """Load all plugins using the simplified system."""
    try:
        manager = PluginsManager()
        manager.load_all_plugins()
        print(f"Loaded plugins at startup: {manager.get_loaded_plugins_count()} total")
    except Exception as e:
        print(f"Error loading plugins at startup: {e}")

# Load plugins when app starts
load_plugins_at_startup()

# ----------------------
# Application startup
if __name__ == '__main__':
    app.run(
        host=APP_SETTINGS.get('HOST', '0.0.0.0'),
        port=APP_SETTINGS.get('PORT', 5000), 
        debug=APP_SETTINGS.get('DEBUG', False)
    )
```

### **FÁZE 6: Testing & Validation**
**Cíl**: Ověřit funkčnost po každé fázi

**Test Checklist**:
- [ ] Plugin loading funguje (24 prompts, 23 workflows, 35 tools)
- [ ] Všechny routes odpovídají stejně jako před refaktoringem
- [ ] Importy fungují bez chyb
- [ ] Hot reload plugin systém funguje
- [ ] PythonAnywhere compatibility (absolutní cesty)

## **Risk Mitigation Strategies**

### **Postupná Migrace**
1. **Jedna fáze v čase**: Implementovat a testovat každou fázi samostatně
2. **Backward compatibility**: Zachovat staré importy během migrace
3. **Rollback plan**: Každá fáze má jasný rollback postup

### **Kritické Import Paths**
**Monitorovat tyto soubory pro import errors**:
- `app/prompts/__init__.py`
- `app/workflows/__init__.py`  
- `app/tools/__init__.py`
- `main.py`
- Všechny plugin soubory

### **PythonAnywhere Compatibility**
**Zajistit funkcionalitu na hosting platformě**:
- Použít absolutní cesty přes `Path(__file__).resolve().parent`
- Testovat path resolution pomocí base classes
- Ověřit že `sys.path` manipulace funguje správně

## **Expected Benefits**

### **🎯 Improved Organization**
- **Logical grouping**: Related files together in `app/core/`
- **Clear separation**: API, UI, Files ve vlastních blueprints
- **Better maintainability**: Snadnější navigace a rozšíření

### **⚡ Enhanced Development Experience**
- **Clean imports**: `from app.core import PluginsManager`
- **Modular routes**: Snadné přidání nových API endpoints
- **Blueprint isolation**: Chyby v jednom blueprintu neovlivní ostatní

### **🛡️ Production Benefits**
- **Better error isolation**: Problémy v blueprintu jsou izolované
- **Easier debugging**: Jasná struktura pro troubleshooting
- **Scalability**: Snadné přidání nových features

## **Implementation Timeline**

### **Doporučené Pořadí Implementace**
1. **Den 1**: Fáze 1 + 2 (Core directory + file moves)
2. **Den 2**: Fáze 3 (Blueprint vytvoření + základní struktura)
3. **Den 3**: Fáze 4 (Import updates + testing)
4. **Den 4**: Fáze 5 (Main.py refactor + route migration)
5. **Den 5**: Fáze 6 (Final testing + validation)

### **Success Criteria**
- ✅ Všechny plugins se načítají bez chyb
- ✅ Všechny web routes fungují identicky
- ✅ Hot-reload system funguje
- ✅ Clean import paths implementovány
- ✅ PythonAnywhere compatibility ověřena

Tento plán zachovává plnou funkčnost současné aplikace při implementaci moderní, škálovatelné architektury s čistým rozdělením zodpovědností.