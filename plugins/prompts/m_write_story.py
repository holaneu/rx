from app.prompts import prompt, render_prompt_with_context

@prompt(name="Write Story", description="Generates short feel-good stories based on simple prompts")
def write_story_v1(*, story_prompt: str):
    """
    Render a prompt for generating a short feel-good story.
    
    Args:
        story_prompt: A brief description, phrase, or situation for the story
    """
    _prompt = """
    Jseš spisovatel krátkých povídek. Uživatel poskytne námět pro krátký příběh ve formě krátké věty, fráze nebo stručného popisu situace. Vytvoř krátký příběh, který bude splňovat tato kritéria:
    - perspektiva: vypravěč (3. osoba)
    - čas: minulý čas, např. "Sam se rozhodl vyrazit ven se projít."
    - postavy: v příběhu se může vyskytovat více postav. Jedna z nich, může to být hlavní nebo vedlejší postava, by měla být muž, věk 39 let, introvert, přemýšlivý, pracuje jako prompt engineer a vývojář python aplikací, otec dvou dětí, ženatý.
    - žánr: fikce ze současnosti (contenporary fiction)
    - pod-žánr: feel-good
    - tón: milý a laskavý, optimistický, s veselou atmosférou, občas humorný
    - dialogy: použij neformální, uvolněný až hovorový tón
    - délka: maximálně 400 slov
    - titulek: název příběhu
    
    Námět pro příběh: {{ story_prompt }}
    
    Vytvoř výstup ve strukturovaném JSON formátu se těmito klíčovými poli:
    - "title": titulek.
    - "content": příběh.
    """
    
    # Automatically merge locals and extra kwargs into context
    return render_prompt_with_context(_prompt.strip(), locals())
