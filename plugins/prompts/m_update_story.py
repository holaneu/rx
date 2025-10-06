from app.prompts import prompt, render_prompt_with_context

@prompt(name="Update Story", description="Updates a story based on editor feedback")
def update_story(*, story: str, editor_feedback: str):
    """
    Render a prompt for updating a story based on editor feedback.
    
    Args:
        story: The original text of the story to be updated
        editor_feedback: The feedback from the editor with instructions for improvement
    """
    _prompt = """
        Jseš spisovatel povídek. Tvým úkolem je upravit původní text povídky přesně podle všech instrukcí k úpravě textu a vytvořit tak novou verzi povídky, ve které budou odstraněny slabé stránky a byla zlepšena kvalita textu. Nepřidávej žádné komentáře ani fráze, ani na začátek, ani na konec tvé odpovědi.

        Původní text:
        {{story}}

        Instrukce k úpravě textu:
        {{editor_feedback}}
        """
    
    return render_prompt_with_context(_prompt.strip(), locals())
