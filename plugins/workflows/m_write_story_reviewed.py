from app.workflows import workflow, Workflow

@workflow()
def write_story_reviewed(input, task_id, model="openai/gpt-4.1"):
    """Generates short feel-good stories reviewed by ai-editor."""

    try:
        wf = Workflow(task_id=task_id)

        from user.tools import save_to_file, user_data_files_path, fetch_llm
        from user.prompts import write_story_v1, review_story, update_story

        # step 1: Generate the story
        story = fetch_llm(input=write_story_v1(story_prompt=input.strip()), model_name=model).get("data", "").get("content", "")

        yield wf.stream_msg(msgTitle="LLM: Story generated", msgBody=str(story))

        # step 2: Get feedback from the editor
        editor_feedback = fetch_llm(input=review_story(story=story.strip()), model_name=model).get("data", "").get("content", "")

        yield wf.stream_msg(msgTitle="LLM: Editor feedback", msgBody=editor_feedback)

        # step 3: Edit the story based on the feedback    
        writer_edited_story = fetch_llm(input=update_story(story=story.strip(), editor_feedback=editor_feedback.strip()), model_name=model).get("data", "").get("content", "")

        yield wf.stream_msg(msgTitle="LLM: Edited story generated", msgBody=writer_edited_story)

        # step 4: Save the story and feedback to file and database
        db_entry = {
            "input": input.strip(),
            "content_for_editor": story.strip(),
            "editor_feedback": editor_feedback.strip(),
            "content": writer_edited_story.strip()        
        }

        user_input1 = yield wf.interaction_request(
            msgTitle="Confirmation required",
            msgBody="Do you want to save the result to file?",
            form_elements=[{"type": "select", "name": "save-confirm", "label": "Do you want to save it?", "options": ["Yes", "No"], "required": True}]
        )

        if user_input1.get("save-confirm") != "Yes":
            return wf.success_response(
                data={"edited_story": writer_edited_story},
                msgBody="Note: Result not saved to file."
            )

        # Save to file
        save_file_result = save_to_file(filepath=user_data_files_path("stories_reviewed.md"), content=db_entry, delimiter="-----", prepend=True)

        yield wf.stream_msg(msg=save_file_result["message"])

        #save_db_result = json_db_add_entry(db_filepath=user_data_files_path("databases/stories.json"), collection="entries", entry=db_entry, add_createdat=True)
        #wf.add_msg_to_log(msg=save_db_result["message"])

        return wf.success_response()
    
    except Exception as e:
        return wf.error_response(error=e)