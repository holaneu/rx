from app.prompts import prompt, render_prompt_with_context


@prompt()
def generate_system_prompt(*, input: str):
    """Generates detailed instructions for different types of assistants."""

    from user.prompts import output_without_comments

    output_format1 = output_without_comments()
    
    _prompt = """**Meta Prompt Text**:
"Based on the provided description, create a role and detailed instructions for an assistant that will perform specific tasks as needed by the user. The resulting text should include the following sections:

1. **Assistant Role**:
    - Clearly define the role the assistant will serve.
    - Describe the overall goal and purpose of the assistant.

2. **Context**:
    - State why this assistant is important and what problem or need it addresses.
    - Mention the context of use (e.g., maintenance of documentation, communication with customers, etc.).

3. **Detailed Task Description**:
    - Describe in detail the procedures and steps the assistant should follow.
    - Each step should be specific and unambiguous, including instructions on how to proceed exactly.
    - Define the inputs the assistant may need and the outputs it should generate.

4. **Example Scenario** (optional):
    - Provide an example situation or interaction where the assistant could be utilized.
    - Examples should demonstrate how the assistant handles a specific task, which may facilitate its implementation.

5. **Principles and Rules**:
    - State the principles the assistant must adhere to (e.g., maintaining structure, adaptability to specific needs).
    - Clarify the limits of the assistant - what it can do and what it cannot.

**Output of the Meta Prompt**:
Based on the user's input, create a clear text that can be directly inserted into the assistant's settings. The text should be structured and sufficiently detailed to allow for easy implementation of the assistant without the need for further modifications.

Output format: {{output_format1}}.

Input: {{ input }}
    """

    return render_prompt_with_context(_prompt.strip(), locals())