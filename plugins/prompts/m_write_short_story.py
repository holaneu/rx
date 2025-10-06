from app.prompts import prompt, render_prompt_with_context

@prompt()
def write_short_story(*, input: str):
    """Generates a short story based on the input theme."""
    
    _prompt = """Create a short story based on the provided theme. The story should be engaging, well-structured, and include:
    - A clear beginning, middle, and end
    - Vivid characters and setting descriptions
    - Meaningful dialogue where appropriate
    - A central conflict or challenge
    - A satisfying resolution
    Keep the narrative concise while maintaining emotional impact and thematic relevance.

    Input: {{ input }}
    """

    return render_prompt_with_context(_prompt.strip(), locals())