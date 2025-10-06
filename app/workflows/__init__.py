
# Expose core functionality directly
from ._core import workflow, Workflow

# --- STATIC IMPORTS (Auto-generated section starts) ---
# AUTO-GENERATED-IMPORTS-START
# AUTO-GENERATED-IMPORTS-END
# --- END OF AUTO GENERATED ---

# Load plugins using simplified system
from app.utils.plugins_manager import PluginsManager
plugins_manager = PluginsManager()
plugins_manager.load_plugins_for_type("workflows")