# Expose core functionality directly
from ._core import tool

# --- STATIC IMPORTS (Auto-generated section starts) ---
# AUTO-GENERATED-IMPORTS-START
# AUTO-GENERATED-IMPORTS-END
# --- END OF AUTO GENERATED ---

# Load plugins using simplified system from new core structure
from app.core import PluginsManager
plugins_manager = PluginsManager()
plugins_manager.load_plugins_for_type("tools")