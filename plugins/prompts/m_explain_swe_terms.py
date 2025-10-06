from app.prompts import prompt, render_prompt_with_context

@prompt()
def explain_swe_terms(*, input: str):
    """Explains a software engineering term in simple words."""

    _prompt = """You are software engineer with expertise in software development and programming. You are given a text that contains a software engineering term. Your task is to explain this term in simple words.
    Output format: Output only the result and dont' write any comments or additional phrases.
    
    Input: {{ input }}
    """

    return render_prompt_with_context(_prompt.strip(), locals())
