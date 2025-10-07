from app.prompts import prompt, render_prompt_with_context

@prompt()
def generate_quiz_json_from_qna(*, source_text: str, questions: str, quiz_id: str, current_datetime: str):
    """Generates quiz questions with answers in json format based on the provided text."""

    source_text = source_text.strip()
    questions = questions.strip()
    
    _prompt = """
Zdrojový text:
{{source_text}}

Otázky:
{{questions}}

Otázky byly vygenerovány na základě zdrojového textu. Pokud je některá otázka nejasná nebo chybná, uprav ji tak, aby byla správná a jednoznačná. 
Dále ke každé otázce přidej dvě další možnosti odpovědí, které budou nesprávné.

Výstup vypiš dle šablony výstupu a nepřidávej žádné další texty, fráze, nebo komentáře.

Šablona výstupu:
{
  "id": {{quiz_id}},
  "name": "<quiz title>",
  "created": {{current_datetime}},
  "tags": ["<topic in one word>"],
  "questions": [
    {
      "question": "<question 1 title>",
      "options": ["<option 1>", "<option 2>", "<option 3>"],
      "answer": <index of one option from options array representing correct answer>
    },
    {
      "question": "<question X title>",
      "options": ["<option 1>", "<option 2>", "<option 3>"],
      "answer": <index of one option from options array representing correct answer>
    }
  ]
}
        
    """

    return render_prompt_with_context(_prompt.strip(), locals())