from app.workflows import workflow, Workflow

@workflow()
def mix_edu_cards(task_id):
    """Processes a text file by splitting its content."""

    try:
        wf = Workflow(task_id=task_id)
        
        from plugins.tools.m_included import open_file, split_clean, save_to_external_file2, formatted_datetime
        from app.configs.app_config import APP_SETTINGS
        import os
        import random            

        files_folder_root = APP_SETTINGS.EXTERNAL_STORAGE_1_LOCAL_PATH
        files_folder_path = "_knowledge_base"
        
        # Define files and their desired item counts
        files_to_process = {
            "manual.md": 1,
            "citim_se_dobre.md": 2,
            "povedlo_se.md": 1,
            "afirmace.md": 5,
            #"aktivity.md": 2,
            #"_for_textio/efektivita.md": 1,
            #"laskavost.md": 2,
            #"_for_textio/reakce.md": 1,
            #"reakce.md": 1
        }

        all_files_content = []
        final_mixed_content = []

        for file_name, items_count in files_to_process.items():
            file_path = os.path.join(files_folder_root, files_folder_path, file_name)
            file_content = open_file(filepath=file_path)
            file_content_splitted = split_clean(content=file_content, delimiter="-----")
            
            # Calculate how many items to pick (min between available items and desired count)
            items_to_pick = min(items_count, len(file_content_splitted))
            selected_items = random.sample(file_content_splitted, items_to_pick)
            
            # Extract the join operation from f-string for Python 3.10 compatibility
            selected_items_text = "\n-----\n".join(selected_items)
            yield wf.stream_msg(msgTitle=f"File '{file_name}': selected items ({items_to_pick}/{len(file_content_splitted)})", msgBody=f"Selected {items_to_pick} items from {len(file_content_splitted)} available:\n\n{selected_items_text}")
            all_files_content.append({file_name: selected_items})
            final_mixed_content.extend(selected_items)
                 
        yield wf.stream_msg(msgTitle=f"Files opened and content splitted: ", msgBody=str(all_files_content))   

        save_result = save_to_external_file2(
                external_root_path=APP_SETTINGS.EXTERNAL_STORAGE_1_LOCAL_PATH,
                filepath=f"_knowledge_base/_for_textio/mixed_cards_{formatted_datetime('%Y%m%d_%H%M%S')}.md",
                content="\n\n-----\n\n".join(final_mixed_content),
                delimiter="-----",
                prepend=False            
            )
        
        yield wf.stream_msg(msg=save_result["message"])

        return wf.success_response(
            data=all_files_content
        )

    except Exception as e:
        return wf.error_response(error=e)