from app.workflows import workflow, Workflow

@workflow()
def snapshot_registries(task_id):
    """Saves a snapshot of the current registries."""
    
    try:
        wf = Workflow(task_id=task_id)
        
        from app.core import WORKFLOWS_REGISTRY, ASSISTANTS_REGISTRY, TOOLS_REGISTRY, PROMPTS_REGISTRY
        import json
        from plugins.tools.m_included import save_to_file, user_data_files_path

        workflows = {
            name: {k: v for k, v in workflow.items() if k != 'function'}
            for name, workflow in sorted(WORKFLOWS_REGISTRY.items())
        }
        workflows_readable = json.dumps(workflows, indent=2, ensure_ascii=False)
        yield wf.stream_msg(msg={"title": f"Workflows Registry Snapshot ({len(workflows)})", "body": workflows_readable})
        #save_to_file(filepath=user_data_files_path("registries/workflows_registry.txt"), content=workflows_readable)

        tools = {
            name: {k: v for k, v in tool.items() if k != 'function'}
            for name, tool in sorted(TOOLS_REGISTRY.items())
        }
        tools_readable = json.dumps(tools, indent=2, ensure_ascii=False)
        yield wf.stream_msg(msg={"title": f"Tools Registry Snapshot ({len(tools)})", "body": tools_readable})
        #save_to_file(filepath=user_data_files_path("registries/tools_registry.txt"), content=tools_readable)

        prompts = {
            name: {k: v for k, v in prompt.items() if k != 'function'}
            for name, prompt in sorted(PROMPTS_REGISTRY.items())
        }
        prompts_readable = json.dumps(prompts, indent=2, ensure_ascii=False)
        yield wf.stream_msg(msg={"title": f"Prompts Registry Snapshot ({len(prompts)})", "body": prompts_readable})
        #save_to_file(filepath=user_data_files_path("registries/prompts_registry.txt"), content=prompts_readable)

        return wf.success_response(data="")
    except Exception as e:
        return wf.error_response(error=e)