from app.workflows import workflow, Workflow

@workflow()
def save_quick_note(input, task_id, model=None):
    """Takes a quick note and saves it to both JSON database and file."""
    try:
        wf = Workflow(task_id=task_id)

        from user.tools import save_to_file, user_data_files_path

        note = input.strip()

        db_entry = {
            "content": note
        }

        file_path = user_data_files_path("quick_notes.md")

        save_file_result = save_to_file(filepath=file_path, content=note, delimiter="-----", prepend=True)

        yield wf.stream_msg(msg=save_file_result["message"])        

        return wf.success_response()
    
    except Exception as e:
        return wf.error_response(error=e)