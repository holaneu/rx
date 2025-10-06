from app.workflows import workflow, Workflow

@workflow()
def generate_theses_from_text(input, task_id, model=None):
    """Exctracts all theses from the input text and saves output to the persistant memory."""

    try:
        wf = Workflow(task_id=task_id)

        from user.tools import save_to_file, user_data_files_path, fetch_llm
        from user.prompts import generate_theses_from_text

        theses = fetch_llm(input=generate_theses_from_text(input=input.strip()), model_name=model).get("data", {}).get("content", "")
        
        yield wf.stream_msg(msgTitle="LLM: Theses extracted", msgBody=theses)

        file_name = "theses_extracted.md"
        user_input1 = yield wf.interaction_request(
            msgTitle="Confirmation required",
            msgBody=f"Do you want to save the result to file '{file_name}'?",
            form_elements=[
                {"type": "select", "name": "file-save-confirm", "label": "Do you want to save it to file?", "options": ["Yes", "No"], "required": True},
            ]
        )      

        if user_input1.get("file-save-confirm") == "Yes":
            file_path = user_data_files_path(file_name)        
            save_file_result = save_to_file(filepath=file_path, content=theses, delimiter="-----", prepend=True)
            yield wf.stream_msg(msg=save_file_result["message"])        

        return wf.success_response()
    
    except Exception as e:
        return wf.error_response(error=e)
