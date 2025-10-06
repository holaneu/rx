from app.workflows import workflow, Workflow

@workflow()
def write_story(input, task_id, model="openai/gpt-4.1"):
    """Generates short feel-good stories."""
    
    try:
        wf = Workflow(task_id=task_id)

        from user.prompts import write_story_v1
        from user.tools import save_to_file, user_data_files_path, fetch_llm

        yield wf.stream_msg(msgTitle="Workflow started", msgBody="Generating story...")        

        story = fetch_llm(input=write_story_v1(story_prompt=input.strip()), model_name=model).get("data", "").get("content", "")

        yield wf.stream_msg(msgTitle="LLM: Story generated", msgBody=story)

        file_name = "stories.md"

        user_input1 = yield wf.interaction_request(
            msgTitle="Confirmation required",
            msgBody=f"Do you want to save the result to file '{file_name}'?",
            form_elements=[
                {"type": "select", "name": "save-confirm", "label": "Do you want to save it?", "options": ["Yes", "No"], "required": True}
            ]
        )

        if user_input1.get("save-confirm") == "Yes": 
            save_file_result = save_to_file(filepath=user_data_files_path(file_name), content=story, delimiter="-----", prepend=True)

            yield wf.stream_msg(msg=save_file_result["message"])

        return wf.success_response()
    
    except Exception as e:
        return wf.error_response(error=e)
