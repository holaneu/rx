from app.prompts import prompt, render_prompt_with_context

@prompt(name="Sarcastic Tech Editor", description="A sarcastic tech editor that generates blog posts with ironic commentary")
def write_sarcastic_tech_editor(*, topic: str, **extra):
    """
    Creates a prompt for a sarcastic tech editor that generates blog posts with ironic commentary.
    
    Args:
        topic: The technical topic to write about
        **extra: Additional context variables
        
    Returns:
        Rendered prompt with context
    """

    _prompt = """
    Jseš redaktor a komentátor technických řešení. Tvým úkolem je napsat blog post na zadané téma. 
    Tvůj styl se vyznačuje schopnosti vidět jednoduchá a funkční řešení a vtipně s dávkou ironie 
    a sarkasmu komentovat postupy a řešení.
    
    Téma: {{ topic }}
    """
    
    # Automatically merge locals and extra kwargs into context
    return render_prompt_with_context(_prompt.strip(), locals(), extra)
