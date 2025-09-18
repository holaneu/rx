---
applyTo: 'app/prompts/**/*.py,user/prompts/**/*.py'
---

# Prompt Module Template
- When asked to create a prompt module, follow this template and create a new .py file with prefix 'm_' followed by the prompt name.
- The function name should match the file name but without the 'm_' prefix.

## File Structure
1. Import the required modules:
```python
from app.prompts import prompt, render_prompt_with_context
```

2. Use the `@prompt()` decorator above your function definition.

3. Define a function with a descriptive name that matches the file name (without the 'm_' prefix).
   - Include a docstring that briefly explains what the prompt does
   - Define parameters with appropriate type hints
   - Use descriptive parameter names, but if only one parameter is needed, name it input

4. Create a `_prompt` string that contains the actual prompt text
   - Use Jinja-style templating with double curly braces: `{{ variable_name }}`
   - Structure the prompt with clear instructions and formatting

5. Return the rendered prompt using `render_prompt_with_context()`

## Example Structure
```python
from app.prompts import prompt, render_prompt_with_context

@prompt()
def your_function_name(*, param1: str, param2: str):
    """A brief description of what this prompt does."""
    
    # Optional: Any pre-processing of input parameters
    param1 = param1.strip()
    
    _prompt = """
    Your prompt text here with templating variables:
    {{ param1 }}
    {{ param2 }}
    """
    
    return render_prompt_with_context(_prompt.strip(), locals())
```

## Complete Examples

### Example 1: Simple Explanation Prompt

```python
from app.prompts import prompt, render_prompt_with_context

@prompt()
def explain_swe_terms(*, input: str):
    """Explains a software engineering term in simple words."""

    _prompt = """You are software engineer with expertise in software development and programming. You are given a text that contains a software engineering term. Your task is to explain this term in simple words.
    Output format: Output only the result and dont' write any comments or additional phrases.
    
    Input: {{ input }}
    """

    return render_prompt_with_context(_prompt.strip(), locals())
```

### Example 2: Complex JSON Generation Prompt

```python
from app.prompts import prompt, render_prompt_with_context

@prompt()
def qna_to_quiz_json(*, source_text: str, questions: str, quiz_id: str, current_datetime: str):
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
```

Follow also [General Coding Instruction](../copilot_instructions.md)