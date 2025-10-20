from app.workflows import workflow, Workflow

@workflow()
def ask_llm_basic(task_id, input, model=None):
    """Ask LLM - input is the whole message"""
    
    try:        
        wf = Workflow(task_id=task_id)

        from plugins.tools.m_included import fetch_llm
        from plugins.tools.m_included import save_to_file, user_data_files_path

        llm_data = fetch_llm(input=input.strip(), model_name=model).get("data", {}).get("content", "")

        yield wf.stream_msg(msgTitle=f"LLM: ", msgBody=str(llm_data))

        file_name = "llm_answers_basic.md"

        user_input1 = yield wf.interaction_request(
            msgTitle="Confirmation required",
            msgBody=f"Do you want to save the result to file '{file_name}'?",
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