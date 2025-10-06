from app.prompts import prompt, render_prompt_with_context


@prompt()
def output_without_comments():
    return "Output only the result and dont' write any comments or additional phrases.."
