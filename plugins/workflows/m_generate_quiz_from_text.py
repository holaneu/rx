from app.workflows import workflow, Workflow

@workflow()
def generate_quiz_from_text(input, task_id, model=None):	
    """
    Processes a text input and generates quiz questions with answers in json format.    
    """
    try:
        wf = Workflow(task_id=task_id)

        from plugins.tools.m_included import save_to_file, user_data_files_path, generate_id, current_datetime_iso, fetch_llm
        from plugins.prompts.m_generate_qna_from_text import generate_qna_from_text
        from plugins.prompts.m_generate_quiz_json_from_qna import generate_quiz_json_from_qna

        questions = fetch_llm(input=generate_qna_from_text(input=input.strip()), model_name=model, structured_output=True).get("data", {}).get("content", "")
        
        yield wf.stream_msg(msgTitle="LLM: QnA from text", msgBody=questions)

        questions_file_path = user_data_files_path("questions_from_text.md")
        
        save_file_result = save_to_file(filepath=questions_file_path, content=questions, delimiter="-----", prepend=True)
        
        yield wf.stream_msg(msg=save_file_result["message"])
        
        quiz_id = generate_id()
        current_datetime = current_datetime_iso()

        quiz_questions = fetch_llm(input=generate_quiz_json_from_qna(source_text=input.strip(), questions=questions, quiz_id=quiz_id, current_datetime=current_datetime), model_name=model, structured_output=True).get("data", {}).get("content", "")
        
        yield wf.stream_msg(msgTitle="LLM: Quiz questions from QnA", msgBody=quiz_questions)

        save_file_result = save_to_file(filepath=user_data_files_path("quizzes.md"), content=quiz_questions, delimiter="-----", prepend=True)

        yield wf.stream_msg(msg=save_file_result["message"])

        return wf.success_response()
    
    except Exception as e:
        return wf.error_response(error=e)