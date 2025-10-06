from app.prompts import prompt, render_prompt_with_context

@prompt(name="Example prompt", description="Showcase task-oriented prompt rendering")
def prompt_example(*, name: str, task: str, projects: list=None, **extra):
    """Render a task-oriented prompt using Jinja2."""
    from datetime import date as dt
    # locals (locar variables) are automatically passed to the template
    var1 = dt.today().strftime("%Y-%m-%d")  # internal variable
    var2 = "some value"  # another internal variable
    _prompt = """
    Hello {{ name }}, today is {{ var1 }}
    Your task: {{ task }}
    {% if projects %}
    You have {{ projects | length }} projects:
    {% for p in projects %}
    - {{ p }}
    {% endfor %}
    {% endif %}
    """
    # Automatically merge locals and extra kwargs into context
    return render_prompt_with_context(_prompt.strip(), locals(), extra)
