from app.prompts import prompt, render_prompt_with_context

@prompt()
def construct_email_ga_event(*, input: str):
    """Generates a developer email with metaHierarchy examples based on GA event specification from email, table, or both."""
    from user.prompts import output_without_comments
    output_format1 = output_without_comments()
    _prompt = """
You are an assistant that receives as input:
- a) copy-pasted data from an Excel table describing GA events, or
- b) an email text containing an inquiry for GA event tracking, or
- c) both email and table combined.

Your task:
1. Analyze the provided input to extract GA event specifications.

2. Identify:
   - The event name(s) (usually in a column like “Event Name”, “Event Action”, “Category”, etc.).
   - Corresponding parameter values (in correct order as in the table or email) — these might be columns like param1, param2, value, label, target path, etc.

3. Generate metaHierarchy lines following this template exactly:
   metaHierarchy["<event name>", "<param 1 value>", "<param 2 value>", ... , "<param N value>"]

   Parameter value placeholder rules:
   - Use placeholders ONLY when the actual value is unknown or variable in the input; if a concrete value is present, use the value (without angle brackets).
   - When a placeholder is needed, write it INSIDE angle brackets: <placeholder>.
   - Keep each placeholder SHORT for readability (ideally 2–5 words), lowercase, snake_case (e.g., <target_path>, <item_id>, <origin>).
   - Do NOT include punctuation inside placeholders (no commas, colons, quotes, or trailing periods).
   - Maintain consistent placeholder names across events when referring to the same concept (e.g., always <item_id>, not <product_id> in one place and <itemId> in another unless the input explicitly distinguishes them).
   - Omit empty parameters entirely — never emit "" or <> for missing/unspecified params.
   - Preserve the parameter ORDER from the specification.

4. Compose the output as a plain-text developer email using the template below.

5. Output rules:
   - Always output the result as markdown.
   - Output ONLY the final developer email with the generated metaHierarchy examples inserted in the correct place.
   - Do NOT add explanations, comments, or extra phrases outside the email body.
   - IMPORTANT: Do NOT wrap the final email in code fences. The output must NOT start or end with ``` and must not contain code blocks.

6. Notes on placeholders section:
   - For EVERY placeholder you used in the metaHierarchy examples, add exactly one bullet explaining it in 1 concise sentence.
   - Use the form: - `<placeholder>`: explanation derived from the input specification.
   - If the input provides a longer/clearer description, summarize it here; keep the placeholder itself short in the metaHierarchy lines.
   - Include bullets ONLY for placeholders actually used in the generated examples.

7. Output format: {{output_format1}}.

## Email template:

Hello, 

This is specification for developers: 

Please can you implement Analytics provider tracking, using "user-action" package from "analytics" repo. This is the common way how to track users' actions among the website, and it has been already used by your team few times. You can find package details here: https://dev.azure.com/oriflame/Web%20Analytics/_git/events

See the metaHierarchy specification of the utilized "user-action" events: 

This is the generic template for metaHierarchy:
metaHierarchy["<event name>", "<param 1 value>", "<param 2 value>", ... , "<param N value>"]

metaHierarchy used:

[INSERT GENERATED metaHierarchy EXAMPLES HERE]

Notes on placeholders:

- [For each placeholder used in the GENERATED metaHierarchy EXAMPLES, insert one bullet in the form `<placeholder>`: <short explanation>. Derive explanations from the input; summarize longer descriptions here.]

Acceptance criteria:

The expected result visible within the browser debug console is this js object pushed into the array var "dataLayer", so this is the way how your QA can test it on UAT / STG / PROD by themselves:  
{ event: "user-action", metaHierarchy["menu_personal_select", "< target path eg. /men etc >"] }

Cooperation:

- Please send me PBI for this task so I can follow it.
- I will also appreciate you to let me know once such PBI is published to production then, so please can you add "Notify Vlada when on PROD" as your team's backlog task 🙂:-) ? Thx a lot!
- If you have any questions, please do not hesitate to ask me.

-----

## Input:
# {{ input }}
"""
    return render_prompt_with_context(_prompt.strip(), locals())
