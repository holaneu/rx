from app.prompts import prompt, render_prompt_with_context

@prompt()
def explain_simply_lexicon(*, input: str):
    _prompt = """Vysvětli pojem tak, aby to pochopilo dítě 4. třídy základní školy.

    <output_template>
    fráze: [vstupní pojem]
    popis: [jednoduché vysvětlení]
    synonyma: [max 4 synonyma oddělená čárkou]
    antonyma: [max 4 antonyma oddělená čárkou]
    příklady:
    - [příklad použití 1]
    - [příklad použití 2]
    - [příklad použití 3]
    </output_template>

    Input: {{ input }}
    """

    return render_prompt_with_context(_prompt.strip(), locals())