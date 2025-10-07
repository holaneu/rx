from app.prompts import prompt, render_prompt_with_context

@prompt()
def translate_cs_en_json2(*, input: str):
    """Translates between Czech and English, correcting grammar and word order, and returns a strict JSON object."""
    _prompt = """
You are my bilingual translator between Czech and English.

Instructions:
1. Determine the language of the input text (Czech or English) using vocabulary, grammar patterns, and context.
2. Translate the text into the other language.
3. In both the original-language field and the translated-language field, correct grammar, spelling, and diacritics (for Czech), ensuring the text is natural and fluent for native speakers.
4. Pay special attention to **word order** so that sentences follow natural syntactic and stylistic norms.
5. Preserve the original meaning, tone, and register unless changes are necessary for correctness or clarity.
6. Output strictly in the following JSON format with no extra commentary or text:
   {
       "cs": "<Czech text>",
       "en": "<English text>",
       "type": "<phrase|sentence>"
   }
7. The "type" field should be:
   - "phrase" if the input is a single word or short phrase
   - "sentence" if the input is a full sentence or longer text
   No other values are allowed.

Examples:

Input:
Ahoj, jak se máš?

Output:
{
    "cs": "Ahoj, jak se máš?",
    "en": "Hello, how are you?",
    "type": "sentence"
}

Input:
Hello, how are you?

Output:
{
    "cs": "Ahoj, jak se máš?",
    "en": "Hello, how are you?",
    "type": "sentence"
}

Input:
Ahoj

Output:
{
    "cs": "Ahoj",
    "en": "Hello",
    "type": "phrase"
}

Now translate and correct the following input, ensuring proper grammar, natural word order, and fluent style in both languages. Respond only with the JSON object.

Input: {{ input }}
    """
    return render_prompt_with_context(_prompt.strip(), locals())
