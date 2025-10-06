from app.workflows import workflow, Workflow

@workflow()
def correct_grammar(task_id, input, model=None):
    """Corrects grammar in the given input text using a language model."""
    
    try:
        wf = Workflow(task_id=task_id)

        from plugins.tools.m_included import fetch_llm
        from plugins.prompts.m_correct_grammar import correct_grammar        

        llm_data = fetch_llm(input=correct_grammar(input=input), model_name=model).get("data", {}).get("content", "")
        
        yield wf.stream_msg(msgTitle=f"LLM: ", msgBody=str(llm_data))

        return wf.success_response()
    
    except Exception as e:
        return wf.error_response(error=str(e))