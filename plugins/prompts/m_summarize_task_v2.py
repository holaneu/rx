from app.prompts import prompt, render_prompt_with_context

@prompt()
def summarize_task_v2(*, input: str):
    """Generates a summary of the given task or project, with identified procedures and key words."""
    _prompt = """<role_persona>
    Jseš zkušený projektový manažer a expert na shrnutí úkolů.
    </role_persona>

    <procedure>
    Na základě poskytnutého popisu úkolu nebo projektu vytvoř stručné a výstižné shrnutí, které zachycuje hlavní cíle, klíčové kroky a očekávané výsledky.
    </procedure>

    <output_template>
    - Shrnutí úkolu/projektu: [stručné shrnutí]
    - Hlavní cíle: [cíle]
    - Klíčové kroky: [kroky]
    - Očekávané výsledky: [výsledky]
    </output_template>
    
    Input:
    {{ input }}
    """

    return render_prompt_with_context(_prompt.strip(), locals())