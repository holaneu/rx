from app.workflows import workflow, Workflow

@workflow()
def summarize_text(input, task_id, model=None):
    """Summarizes input text."""

    try:
        wf = Workflow(task_id=task_id)

        from plugins.tools.m_included import save_to_file, user_data_files_path, fetch_llm
        from plugins.prompts.m_summarize_text_key_takeaways import summarize_text_key_takeaways

        ai_data = fetch_llm(input=summarize_text_key_takeaways(input=input.strip()), model_name=model).get("data", {}).get("content", "")

        yield wf.stream_msg(msgTitle="LLM: Summary generated", msgBody=ai_data)

        file_path = user_data_files_path("summaries.md")
        save_file_result = save_to_file(filepath=file_path, content=ai_data, delimiter="-----", prepend=True)
        yield wf.stream_msg(msg=save_file_result["message"])

        return wf.success_response(
            data=""
        )
    except Exception as e:
        return wf.error_response(error=e)