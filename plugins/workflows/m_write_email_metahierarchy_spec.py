from app.workflows import workflow, Workflow

@workflow()
def write_email_metahierarchy_spec(task_id, input, model=None):
    """Generates a metahierarchy specification for an email workflow using an LLM."""
    
    try:
        wf = Workflow(task_id=task_id)
        
        from plugins.tools.m_included import fetch_llm
        from plugins.prompts.m_construct_email_ga_event import construct_email_ga_event

        llm_data = fetch_llm(input=construct_email_ga_event(input=input), model_name=model).get("data", {}).get("content", "")

        yield wf.stream_msg(msgTitle=f"LLM: ", msgBody=str(llm_data))

        return wf.success_response()
    
    except Exception as e:
        return wf.error_response(error=str(e))