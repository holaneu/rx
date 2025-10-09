"""Enhanced script to fix all remaining user.* imports."""

import re
from pathlib import Path

def fix_remaining_imports():
    """Fix all remaining user.* imports in plugin files."""
    
    # Enhanced mapping for remaining imports
    import_mappings = {
        # More prompt imports
        r'from user\.prompts import generate_theses_from_text': 'from plugins.prompts.m_generate_theses_from_text import generate_theses_from_text',
        r'from user\.prompts import generate_system_prompt': 'from plugins.prompts.m_generate_system_prompt import generate_system_prompt',
        r'from user\.prompts import generate_qna_from_text, generate_quiz_json_from_qna': 'from plugins.prompts.m_generate_qna_from_text import generate_qna_from_text\n        from plugins.prompts.m_generate_quiz_json_from_qna import generate_quiz_json_from_qna',
        r'from user\.prompts import explain_swe_terms': 'from plugins.prompts.m_explain_swe_terms import explain_swe_terms',
        r'from user\.prompts import explain_simply_lexicon': 'from plugins.prompts.m_explain_simply_lexicon import explain_simply_lexicon',
        r'from user\.prompts import correct_grammar': 'from plugins.prompts.m_correct_grammar import correct_grammar',
        r'from user\.prompts import analyze_situation': 'from plugins.prompts.m_analyze_situation import analyze_situation',
        r'from user\.prompts import output_without_comments': 'from plugins.prompts.m_output_without_comments import output_without_comments',
        
        # Tools imports
        r'from user\.tools import (.+)': r'from plugins.tools.m_included import \1',
    }
    
    # Find all plugin files
    plugins_dir = Path('plugins')
    all_files = []
    all_files.extend(list(plugins_dir.glob('workflows/m_*.py')))
    all_files.extend(list(plugins_dir.glob('prompts/m_*.py')))
    all_files.extend(list(plugins_dir.glob('tools/m_*.py')))
    
    print(f"Found {len(all_files)} plugin files to check")
    
    for file_path in all_files:
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

def fix_core_files():
    """Fix imports in core app files."""
    
    print("\\n=== Fixing core app files ===")
    
    # Fix app/workflows/_core.py
    core_file = Path('app/workflows/_core.py')
    if core_file.exists():
        print(f"Processing {core_file}")
        
        try:
            with open(core_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Replace the user.tools import
            content = re.sub(
                r'from user\.tools\.m_included import (.+)',
                r'from plugins.tools.m_included import \1',
                content
            )
            
            with open(core_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"  Updated {core_file}")
            
        except Exception as e:
            print(f"  Error processing {core_file}: {e}")

if __name__ == "__main__":
    fix_remaining_imports()
    fix_core_files()
    print("\\nAll import fixing completed!")