from app.workflows import workflow, Workflow

@workflow()
def ask_llm_basic(task_id, input, model=None):
    """Ask LLM - input is the whole message"""
    
    try:        
        wf = Workflow(task_id=task_id)

        from user.tools import fetch_llm

        llm_data = fetch_llm(input=input.strip(), model_name=model).get("data", {}).get("content", "")

        yield wf.stream_msg(msgTitle=f"LLM: ", msgBody=str(llm_data))

        return wf.success_response()
    
    except Exception as e:
        return wf.error_response(error=str(e))