from app.workflows import workflow, Workflow

@workflow()
def translate_cs_en_basic(task_id, input, model="openai/gpt-4.1"):
    """Translates text between Czech and English v2."""

    try:
        wf = Workflow(task_id=task_id)

        from plugins.tools.m_included import save_to_file, user_data_files_path, fetch_llm
        from plugins.prompts.m_translate_cs_en_basic import translate_cs_en_basic
        from plugins.prompts.m_correct_grammar import correct_grammar

        yield wf.stream_msg(msgTitle="Workflow Started", msgBody=f"Task ID: {task_id}, Input: {input}, Model: {model}")

        translated_text = fetch_llm(input=translate_cs_en_basic(input=input.strip()), model_name=model).get("data", {}).get("content", "")

        yield wf.stream_msg(msgTitle="LLM: Translated text", msgBody=translated_text)

        translated_text_corrected = fetch_llm(input=correct_grammar(input=translated_text.strip()), model_name=model).get("data", {}).get("content", "")

        yield wf.stream_msg(msgTitle="LLM: Translated text (corrected grammar)", msgBody=translated_text_corrected)

        file_name = "translations_basic.md"

        user_input1 = yield wf.interaction_request(
            msgTitle="Confirmation required",
            msgBody=f"Do you want to save the result to file '{file_name}'?",
            form_elements=[
                {"type": "select", "name": "file-save-confirm", "label": "Do you want to save it to file?", "options": ["Yes", "No"], "required": True},
            ]
        )

        if user_input1.get("file-save-confirm") == "Yes":
            save_file_result = save_to_file(filepath=user_data_files_path(file_name), content=translated_text_corrected, delimiter="-----", prepend=True)

            yield wf.stream_msg(msg=save_file_result["message"])

        """if user_input1.get("db-save-confirm") == "Yes":
            save_db_result = json_db_add_entry(db_filepath=user_data_files_path(f"databases/vocabulary.json"), collection="entries", entry=ai_data_parsed, add_createdat=True)
            wf.log_msg(msg=save_db_result["message"])  """

        return wf.success_response()

        """
        file_path = user_data_files_path("translations_basic.md")
        save_file_result = save_to_file(filepath=file_path, content=translated_text, delimiter="-----", prepend=True)
        yield wf.stream_msg(msg=save_file_result["message"])

        return wf.success_response()
        """

    except Exception as e:
        return wf.error_response(error=e)