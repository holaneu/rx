from app.workflows import workflow, Workflow

@workflow()
def translate_cs_en_json(input, task_id, model="openai/gpt-4.1"):
    """Translates text between Czech and English and outputs it in JSON format."""    
    
    try:
        wf = Workflow(task_id=task_id)

        from plugins.tools.m_included import save_to_file, user_data_files_path, fetch_llm
        from plugins.prompts.m_translate_cs_en_json2 import translate_cs_en_json2
        import json

        yield wf.stream_msg(msgTitle="Workflow Started", msgBody=f"Model: {model}")

        ai_data = fetch_llm(input=translate_cs_en_json2(input=input), model_name=model, structured_output=True).get("data", {}).get("content", "")
        
        yield wf.stream_msg(msgTitle="LLM: Translation 1", msgBody=ai_data)

        ai_data_parsed = json.loads(ai_data)
        if not isinstance(ai_data_parsed, dict):
            raise Exception("invalid JSON structure")

        ai_data_readable = json.dumps(ai_data_parsed, indent=2, ensure_ascii=False)

        file_name = "vocabulary_json.md"

        user_input1 = yield wf.interaction_request(
            msgTitle="Confirmation required",
            msgBody=f"Do you want to save the result to file '{file_name}'?",
            form_elements=[
                {"type": "select", "name": "file-save-confirm", "label": "Do you want to save it to file?", "options": ["Yes", "No"], "required": True},
            ]
        )

        if user_input1.get("file-save-confirm") == "Yes":
            save_file_result = save_to_file(filepath=user_data_files_path(file_name), content=ai_data_readable, delimiter="-----", prepend=True)

            yield wf.stream_msg(msg=save_file_result["message"])

        """if user_input1.get("db-save-confirm") == "Yes":
            save_db_result = json_db_add_entry(db_filepath=user_data_files_path(f"databases/vocabulary.json"), collection="entries", entry=ai_data_parsed, add_createdat=True)
            wf.log_msg(msg=save_db_result["message"])  """

        return wf.success_response()
    
    except Exception as e:
        return wf.error_response(error=str(e))