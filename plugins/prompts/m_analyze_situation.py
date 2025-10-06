from app.prompts import prompt, render_prompt_with_context


@prompt()
def analyze_situation(*, input: str):
    """Analyzuje popsanou situaci a vytváří strukturovaný přehled."""
    _prompt = """<role_persona>
    Jseš expert na analýzu situací a jejich rozbor.
    </role_persona>

    <procedure>
    Analyzuj popsanou situaci a vytvoř strukturovaný přehled obsahující:
    - Shrnutí celé situace
    - Informace o jednotlivých účastnících včetně jejich:
      - Rolí
      - Motivů
      - Záměrů
      - Cílů
      - Akcí
      - Pocitů
    </procedure>

    <output_template>
    - Situace: [popis]
    - Shrnutí situace: [stručné shrnutí]
    - Účastnící:
      - [účastník]:
        - Role: [role]
        - Motiv: [motiv]
        - Záměr: [záměr]
        - Cíl: [cíl]
        - Akce: [akce]
        - Pocity: [pocity]
    </output_template>
    
    Input:
    {{ input }}
    """

    return render_prompt_with_context(_prompt.strip(), locals())
