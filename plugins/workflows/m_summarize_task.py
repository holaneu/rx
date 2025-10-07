from app.workflows import workflow, Workflow

@workflow()
def summarize_task(input, task_id, model=None):
    """Writes a logbook entry."""
    try:
        wf = Workflow(task_id=task_id)

        from plugins.tools.m_included import save_to_file, user_data_files_path, fetch_llm
        from plugins.prompts.m_summarize_task import summarize_task
        import json
        
        entry = fetch_llm(input=summarize_task(input=input.strip()), model_name=model, structured_output=True).get("data", {}).get("content", "")

        yield wf.stream_msg(msgTitle="LLM: task summary", msgBody=entry)
        
        file_name = "journal_task_summaries.md"
        
        user_input1 = yield wf.interaction_request(
            msgTitle="Confirmation required",
            msgBody=f"Do you want to save the result to file '{file_name}'?",
            form_elements=[
                {"type": "select", "name": "file-save-confirm", "label": "Do you want to save it to file?", "options": ["Yes", "No"], "required": True},
            ]
        )      

        if user_input1.get("file-save-confirm") == "Yes":
            try:
                entry_parsed = json.loads(entry)
                if not isinstance(entry_parsed, dict):
                    return "invalid JSON structure"
                # Save pretty-printed JSON to file
                entry_str = json.dumps(entry_parsed, indent=2, ensure_ascii=False)

                save_file_result = save_to_file(filepath=user_data_files_path(file_name), content=entry_str, delimiter="-----", prepend=True)
                yield wf.stream_msg(msg=save_file_result["message"])

                return wf.success_response()        
        
            except json.JSONDecodeError:
                raise Exception("failed to decode JSON")
    
    except Exception as e:
        return wf.error_response(error=e)

