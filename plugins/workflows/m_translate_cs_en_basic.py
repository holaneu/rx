from app.workflows import workflow, Workflow

@workflow()
def translate_cs_en_basic(task_id, input, model="openai/gpt-4.1"):
    """Translates text between Czech and English v2."""

    try:
        wf = Workflow(task_id=task_id)

        from user.tools import save_to_file, user_data_files_path, fetch_llm
        from user.prompts import translate_cs_en_basic

        yield wf.stream_msg(msgTitle="Workflow Started", msgBody=f"Task ID: {task_id}, Input: {input}, Model: {model}")

        translated_text = fetch_llm(input=translate_cs_en_basic(input=input.strip()), model_name=model).get("data", {}).get("content", "")

        yield wf.stream_msg(msgTitle="LLM: Translated text", msgBody=translated_text)

        file_path = user_data_files_path("translations_basic.md")
        save_file_result = save_to_file(filepath=file_path, content=translated_text, delimiter="-----", prepend=True)

        yield wf.stream_msg(msg=save_file_result["message"])

        return wf.success_response()

    except Exception as e:
        return wf.error_response(error=e)