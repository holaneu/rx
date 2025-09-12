
# Expose directly
from ._core import workflow, Workflow

# --- STATIC IMPORTS (Auto-generated section starts) ---
# AUTO-GENERATED-IMPORTS-START
# AUTO-GENERATED-IMPORTS-END
# --- END OF AUTO GENERATED ---

# Load user-defined modules for this package using new system
from app.configs.module_config import ModuleConfig, PackageTypes
config = ModuleConfig()
registry = config.get_registry_for_package(PackageTypes.WORKFLOWS.value)
if registry is not None:
    from app.utils.module_manager import ModuleManager
    manager = ModuleManager()
    manager._load_dynamic_modules_for_package(PackageTypes.WORKFLOWS.value, registry)