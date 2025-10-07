from app.workflows import workflow, Workflow

@workflow()
def generate_system_prompt(input, task_id, model=None):
    """Creates a new assistant based on the input."""
    
    try:
        wf = Workflow(task_id=task_id)

        from plugins.tools.m_included import save_to_file, user_data_files_path, fetch_llm
        from plugins.prompts.m_generate_system_prompt import generate_system_prompt

        ai_data = fetch_llm(input=generate_system_prompt(input=input), model_name=model).get("data", {}).get("content", "")
        
        yield wf.stream_msg(msgTitle="LLM: prompt generated", msgBody=ai_data)

        file_name = "system_prompts.md"
        
        user_input1 = yield wf.interaction_request(
            msgTitle="Confirmation required",
            msgBody=f"Do you want to save the result to file '{file_name}'?",
            form_elements=[
                {"type": "select", "name": "file-save-confirm", "label": "Do you want to save it to file?", "options": ["Yes", "No"], "required": True},
            ]
        )        

        if user_input1.get("file-save-confirm") == "Yes":
            
            save_file_result = save_to_file(filepath=user_data_files_path(file_name), content=ai_data, delimiter="-----", prepend=True)

            yield wf.stream_msg(msg=save_file_result["message"])

        return wf.success_response()
    
    except Exception as e:

        return wf.error_response(error=e)
