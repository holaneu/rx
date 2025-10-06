from app.prompts import prompt, render_prompt_with_context

@prompt()
def summarize_task(*, input: str):
    """Generates a summary of the given task or project, with identified procedures and key words."""

    _prompt = """Na základě zadaného vstupu (může jít o větu, poznámku nebo kus kódu) vytvoř výstup ve strukturovaném JSON formátu se třemi klíčovými poli:
    - "summary": Shrň, co daný úkol nebo kód dělá z pohledu uživatele (co mu to přinese nebo umožní). Pokud se jedná o kód, na začátek věty dej "Kód který, " (např. "Kód, který převede YAML na JSON").
    - "procedure": V bodech popiš, co se děje krok za krokem. Každý bod formuluj jednoduše tak, aby mu rozuměl i netechnický čtenář. Za popis připoj do závorky krátké technické vysvětlení nebo zmínku o použitých funkcích, pokud to dává smysl. Pokud se jedná o kód, je preferované uvést do závorku funkci či metodu. Tam kde to dává smysl, např. pokud se jedná o kód, použij infinitivní slovesa bez podmětu (např. "Vybrat nejvhodnější výsledek ...", "Stáhnout obsah z ..." atd.). 
    - "key_words": Vyjmenuj nejdůležitější použité technologie, knihovny, metody nebo klíčové pojmy. Vypisuj pouze ty, které vystihují účel a průběh úkolu nebo kódu.

    Použij výstupní formát JSON, např.:
    {
    "summary": "...",
    "procedure": [
        "...",
        "..."
    ],
    "key_words": [
        "...",
        "..."
    ]
    }

    Vstup:
    {{input}}

    Priklady:
    Priklad vstupu:
    import json
    data = {"name": "Alice", "age": 30}
    json_string = json.dumps(data)
    print(json_string)

    Priklad vystupu:
    {
    "summary": "Kód, který převede slovník s údaji o osobě na JSON řetězec a zobrazí ho.",
    "procedure": [
        "Načíst knihovnu pro práci s JSON formátem (import json).",
        "Vytvořit slovník s informacemi o osobě, jako je jméno a věk (data = {{...}}).",
        "Převést slovník na textový formát JSON (json.dumps()).",
        "Vypsat výsledný JSON řetězec do konzole (print())."
    ],
    "key_words": [
        "Python",
        "json.dumps()",
        "slovník",
        "JSON"
    ]
    }
    """

    return render_prompt_with_context(_prompt.strip(), locals())