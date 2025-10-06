import os
from pathlib import Path
from dotenv import load_dotenv

# Use pathlib for more robust path handling
_config_dir = Path(__file__).parent
_app_root = _config_dir.parent.parent
load_dotenv(dotenv_path=_app_root / '.env')

# settings:

class USER_SETTINGS:
    USER_ID = "admin" # !!! Don't change this value !!!

class APP_SETTINGS:
    # Use pathlib for cross-platform path handling
    _APP_ROOT = Path(__file__).parent.parent.parent
    USER_DATA_PATH = _APP_ROOT / "user"
    USER_DATA_FILES_PATH = _APP_ROOT / "user" / "files"
    
    # String versions for backward compatibility where needed
    USER_DATA_PATH_STR = str(USER_DATA_PATH)
    USER_DATA_FILES_PATH_STR = str(USER_DATA_FILES_PATH)
    
    EXTERNAL_STORAGE_1_LOCAL_PATH = os.getenv("EXTERNAL_STORAGE_1_LOCAL_PATH")
    CUSTOM_MODULES_FOLDERS = ["workflows", "prompts", "tools"]
    
