"""Script to fix old user.* imports in plugin files."""

import re
from pathlib import Path

def fix_user_imports():
    """Fix all user.* imports in plugin files."""
    
    # Define the mapping from old user imports to new plugin imports
    import_mappings = {
        # Tools imports
        r'from user\.tools import (.+)': r'from plugins.tools.m_included import \1',
        
        # Individual prompt imports - need to map to specific files
        r'from user\.prompts import write_story_v1': 'from plugins.prompts.m_write_story import write_story_v1',
        r'from user\.prompts import review_story': 'from plugins.prompts.m_review_story import review_story', 
        r'from user\.prompts import update_story': 'from plugins.prompts.m_update_story import update_story',
        r'from user\.prompts import translate_cs_en_json2': 'from plugins.prompts.m_translate_cs_en_json2 import translate_cs_en_json2',
        r'from user\.prompts import translate_cs_en_yaml': 'from plugins.prompts.m_translate_cs_en_yaml import translate_cs_en_yaml',
        r'from user\.prompts import translate_cs_en_basic': 'from plugins.prompts.m_translate_cs_en_basic import translate_cs_en_basic',
        r'from user\.prompts import summarize_video_transcript': 'from plugins.prompts.m_summarize_video_transcript import summarize_video_transcript',
        r'from user\.prompts import summarize_text_key_takeaways': 'from plugins.prompts.m_summarize_text_key_takeaways import summarize_text_key_takeaways',
        r'from user\.prompts import summarize_task': 'from plugins.prompts.m_summarize_task import summarize_task',
        r'from user\.prompts import construct_email_ga_event': 'from plugins.prompts.m_construct_email_ga_event import construct_email_ga_event',
    }
    
    # Find all workflow files that need fixing
    plugins_dir = Path('plugins')
    workflow_files = list(plugins_dir.glob('workflows/m_*.py'))
    
    print(f"Found {len(workflow_files)} workflow files to check")
    
    for file_path in workflow_files:
        print(f"\\nProcessing {file_path}")
        
        try:
            # Read the file
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Apply all mappings
            for pattern, replacement in import_mappings.items():
                content = re.sub(pattern, replacement, content)
            
            # Check if anything changed
            if content != original_content:
                print(f"  Updated imports in {file_path.name}")
                
                # Write back the updated content
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
            else:
                print(f"  No changes needed in {file_path.name}")
                
        except Exception as e:
            print(f"  Error processing {file_path}: {e}")

if __name__ == "__main__":
    fix_user_imports()
    print("\\nImport fixing completed!")