from app.prompts import prompt, render_prompt_with_context

@prompt()
def generate_theses_from_text(*, input: str):
    """Extracts the thesis statement from the given input text."""

    _prompt = """Analyzuj zdrojový text a extrahuj všechny tvrzení (teze) ze zdrojového textu a vypiš je ve strukturovaných bodech. Teze jsou krátké výroky, které shrnují hlavní myšlenku nebo obsah textu. Zajisti úplnost extrakce bez vynechání jakékoli teze. Zachovej původní význam, důležité informace a přesnost formulací. Používej samostatné teze tzn. rozděl složené teze na jednotlivé samostatné teze. Nepřidávej žádné komentáře ani fráze, ani na začátek, ani na konec tvé odpovědi.

    Vstupní text:
    {{input}}

    Výstup:
    - [teze 1]
    - [teze 2]
    - [teze 3]
    """
    
    return render_prompt_with_context(_prompt.strip(), locals())