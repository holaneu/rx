from app.prompts import prompt, render_prompt_with_context

@prompt(name="Review Story", description="Reviews stories and provides feedback for improvement")
def review_story(*, story: str):
    """
    Render a prompt for getting professional story review and improvement suggestions.
    
    Args:
        story: The text of the story to be reviewed
    """
    _prompt = """Jseš profesionální editor povídek, který posuzuje povídky a poskytuje zpětnou vazbu k jejich úpravě a zlepšení. Analyzuj vstupní text povídky a její slabé stránky a napiš jasné a stručné doporučení jak text upravit tak aby se odstranily tyto slabé stránky. Doporučení piš formou odrážek v neformátovaném plain text formátu. Nepřidávej žádné komentáře ani fráze, ani na začátek, ani na konec tvé odpovědi.

        Vstupní text:
        {{story}}
    """
    
    # Automatically merge locals and extra kwargs into context
    return render_prompt_with_context(_prompt.strip(), locals())
