from app.prompts import prompt, render_prompt_with_context


@prompt()
def correct_grammar(*, input: str, extra_instructions: str = None):
    """Corrects grammar where needed and returns corrected text"""
    from user.prompts import output_without_comments
    output_format1 = output_without_comments()
    _prompt = """    
Instructions: 
1. Carefully and accurately identify the language of the Input text (Input). Use all available clues, including vocabulary, grammar patterns, and context, to ensure correct detection.
2. Based on the identified language, correct the grammar while preserving the original meaning.
3. Pay special attention to word order so that it follows the natural syntactic and stylistic norms of the identified language, ensuring the text reads naturally to a native speaker.
4. Avoid altering meaning, tone, or register unless necessary for grammatical correctness or natural flow.

{% if extra_instructions %}
Extra instructions: {{ extra_instructions }}
{% endif %}

Input:
{{ input }}

Output format:
{{ output_format1 }}
"""

    return render_prompt_with_context(_prompt.strip(), locals())
