from app.workflows import workflow, Workflow

@workflow()
def write_sarcastic_tech_editor(task_id, input, model=None):
    """Generate a sarcastic tech blog post on the given topic"""
    
    try:        
        wf = Workflow(task_id=task_id)

        from user.tools import fetch_llm, save_to_file, user_data_files_path
        from app.prompts.m_sarcastic_tech_editor import sarcastic_tech_editor
        
        # Fetch response from LLM
        llm_data = fetch_llm(input=sarcastic_tech_editor(topic=input.strip()), model_name=model).get("data", {}).get("content", "")

        # Stream the response
        yield wf.stream_msg(msgTitle=f"LLM: Sarcastic Tech Editor", msgBody=str(llm_data))

        file_name = "sarcastic_tech_commentary.md"
        user_input1 = yield wf.interaction_request(
            msgTitle="Confirmation required",
            msgBody=f"Do you want to save the result to the file '{file_name}'?",
            form_elements=[
                {"type": "select", "name": "file-save-confirm", "label": "Do you want to save it to file?", "options": ["Yes", "No"], "required": True},
            ]
        )

        if user_input1.get("file-save-confirm") == "Yes":
            save_file_result = save_to_file(filepath=user_data_files_path(file_name), content=llm_data, delimiter="-----", prepend=True)
            
            yield wf.stream_msg(msg=save_file_result["message"])

        return wf.success_response()
    
    except Exception as e:
        return wf.error_response(error=str(e))
