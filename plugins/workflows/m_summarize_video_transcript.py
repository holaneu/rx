from app.workflows import workflow, Workflow

@workflow()
def summarize_video_transcript(input, task_id, model=None):
    """Summarizes the transcript of a video."""
    
    try:
        wf = Workflow(task_id=task_id)

        from user.tools import save_to_file, user_data_files_path, fetch_llm
        from user.prompts import summarize_video_transcript

        ai_data = fetch_llm(input=summarize_video_transcript(input=input.strip()), model_name=model ).get("data", {}).get("content", "")

        yield wf.stream_msg(msgTitle="LLM: Transcript summary generated", msgBody=ai_data)

        file_name = "video_transcript_summaries.md"
        save_file_result = save_to_file(filepath=user_data_files_path(file_name), content=ai_data, delimiter="-----", prepend=True)

        yield wf.stream_msg(msg=save_file_result["message"])

        return wf.success_response()
    
    except Exception as e:
        return wf.error_response(error=e)