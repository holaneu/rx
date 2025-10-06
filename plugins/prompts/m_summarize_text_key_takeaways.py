from app.prompts import prompt, render_prompt_with_context

@prompt()
def summarize_text_key_takeaways(*, input: str):
    """Summarizes the input text with key takeaways in a concise format."""
    _prompt = """
Your task is to generate a concise summary of the key takeaways from the provided text.

Instructions:
- Focus on the most important points, ideas, or arguments in the text.
- Create a clear, concise summary that accurately represents the main ideas.
- Avoid unnecessary details or personal interpretations.
- Provide a brief overview that captures the essence of the text.
- Use simplified language whenever possible.
- Organize key points in a logical structure.
- Maintain the original meaning while condensing the content.

Now, please summarize the following text with its key takeaways:

{{ input }}
    """

    # original prompt:
    """Your task is to generate a concise summary of the key takeaways from the provided text. Focus on the most important points, ideas, or arguments. Your summary should be clear, concise, and accurately represent the main ideas. Avoid unnecessary details or personal interpretations. Provide a brief overview that captures the essence of the text. Use simplified language whenever possible.
    """

    return render_prompt_with_context(_prompt.strip(), locals())
