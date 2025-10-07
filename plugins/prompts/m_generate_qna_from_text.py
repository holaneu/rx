from app.prompts import prompt, render_prompt_with_context

@prompt()
def generate_qna_from_text(*, input: str):
    """Generates questions with answers in json format based on the provided text."""

    input = input.strip()
    
    _prompt = """Na základě zdrojového textu napiš otázky, které se ptají na podstatné informace uvedené ve zdrojovém textu. Přidej ke každé otázce také stručnou odpověď. Pravidla: 
Na každou otázku bude vždy pouze jedna jednoznačná správná odpověď. 
Používej samostatné otázky tzn. rozděl složené otázky na jednotlivé samostatné otázky, aby nebylo nutné odpovídat na více věcí najednou.

<output_format>
- [otázka 1] ([odpověď na otázku 1])
- [otázka 2] ([odpověď na otázku 2])
- [otázka 3] ([odpověď na otázku 3])
...
</output_format>

<example>
Zdroj: Nejdelší řeka ČR je Vltava. Nejvýznamnější přítoky řeky Vltavy jsou Berounka a Sázava. Vltava se vlévá do řeky Labe ve městě Mělník.

Otázky:
- Jaké je nejdelší řeka v ČR? (Vltava)
- Jaké jsou nejvýznamnější přítoky Vltavy? (Berounka a Sázava)
- Do jaké řeky se vlévá Vltava? (Labe)
- Ve kterém městě se nachází soutok Vltavy a Labe? (Mělník)
</example>

Zdrojový text:
{{input}}
    """

    return render_prompt_with_context(_prompt.strip(), locals())