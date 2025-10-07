from app.workflows import workflow, Workflow

@workflow()
def translate_cs_en_yaml(input, task_id, model=None):
    """Translates text between Czech and English in YAML format."""

    try:
        wf = Workflow(task_id=task_id)

        from plugins.tools.m_included import save_to_file, user_data_files_path, fetch_llm        
        from plugins.prompts.m_translate_cs_en_yaml import translate_cs_en_yaml

        ai_data = fetch_llm(input=translate_cs_en_yaml(input=input), model_name=model).get("data", {}).get("content", "")

        yield wf.stream_msg(msgTitle="LLM: Translation", msgBody=ai_data)

        file_path = user_data_files_path("vocabulary_yaml.md")
        save_file_result = save_to_file(filepath=file_path, content=ai_data, delimiter="-----", prepend=True)
        
        yield wf.stream_msg(msg=save_file_result["message"])

        return wf.success_response()
    
    except Exception as e:
        return wf.error_response(error=e)