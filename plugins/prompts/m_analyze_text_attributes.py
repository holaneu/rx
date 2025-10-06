from app.prompts import prompt, render_prompt_with_context

@prompt()
def analyze_text_attributes(*, input: str):
    """Analyzes text and provides general characteristics like style, theme, tone, length, and expertise level."""

    _prompt = """Analyzuj text a napiš jeho obecnou charakteristiku (styl, téma, délka, tón, míra odbornosti) v odrážkách.

    <output_template>
    téma:
    styl:
    tón:
    délka:
    míra odbornosti: <číslené skóre odbornosti v daném tématu od 1 do 10, kde 10 je nejvíce odborné>
    </output_template>.

    Input: {{ input }}
    """

    return render_prompt_with_context(_prompt.strip(), locals())