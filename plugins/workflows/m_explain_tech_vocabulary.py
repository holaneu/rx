from app.workflows import workflow, Workflow

@workflow()
def explain_tech_vocabulary(task_id, model="openai/gpt-4.1-mini"):
    """Auto explain technical vocabulary terms from a file."""
    
    try:
        wf = Workflow(task_id=task_id)
        
        from plugins.tools.m_included import open_file, split_clean, fetch_llm, save_to_external_file2
        from plugins.prompts.m_explain_swe_terms import explain_swe_terms
        from app.configs.app_config import APP_SETTINGS
        from app.utils.response_types import ResponseKey, ResponseStatus

        from pathlib import Path

        files_folder_root = APP_SETTINGS.EXTERNAL_STORAGE_1_LOCAL_PATH
        
        # Check if external storage path is configured
        if not files_folder_root:
            raise ValueError(f"EXTERNAL_STORAGE_1_LOCAL_PATH is not configured in APP_SETTINGS. Value: {files_folder_root}")
        
        # Convert to Path and validate
        try:
            files_folder_root_path = Path(files_folder_root)
        except (TypeError, ValueError) as e:
            raise ValueError(f"Invalid EXTERNAL_STORAGE_1_LOCAL_PATH: {files_folder_root}. Error: {e}")
        
        files_folder_path = "_knowledge_base"
        input_file_name = "vocabulary_tech"
        input_file_extension = ".md"
        
        # Construct path step by step for better error tracking
        try:
            input_file_path = files_folder_root_path / files_folder_path / (input_file_name + input_file_extension)
        except Exception as e:
            raise ValueError(f"Failed to construct input file path. Root: {files_folder_root_path}, Folder: {files_folder_path}, File: {input_file_name + input_file_extension}. Error: {e}")

        # Use Python's built-in open() for external storage files since open_file() is restricted to user data path
        try:
            with input_file_path.open('r', encoding='utf-8') as f:
                input_file = f.read()
        except Exception as e:
            raise ValueError(f"Failed to read input file: {input_file_path}. Error: {e}")
        
        input_file_content_splitted = split_clean(content=input_file, delimiter="-----")

        input_file_content_transformed = []

        # transform input file content into a list of dictionaries
        # each dictionary contains 'term' and 'explanation' keys
        # IMPORTANT: Process in original order to maintain record sequence
        for i, item in enumerate(input_file_content_splitted):        
            parts = split_clean(content=item, delimiter="==")
            item_dict = {
                "original_index": i,  # Track original position
                "term": parts[0].strip(), 
                "explanation": parts[1].strip() if len(parts) > 1 else ""
            }
            input_file_content_transformed.append(item_dict)

        yield wf.stream_msg(msg={"title": f"File loaded - total terms: {len(input_file_content_transformed)}", "body": str(input_file_content_transformed)})

        # Process each term and explanation IN ORIGINAL ORDER
        # Create a copy of the list to avoid modifying during iteration
        items_to_process = input_file_content_transformed.copy()
        items_without_explanation = 0
        items_explained = 0


        for item in items_to_process:
            term = item["term"]
            explanation = item.get("explanation", "").strip()
            
            # Only process terms that have no explanation or empty explanation
            if not explanation:
                items_without_explanation += 1
                #yield wf.stream_msg(msg={"title": f"Processing unexplained term: '{term}'", "body": "Fetching explanation from LLM..."})
                
                # If no explanation, fetch it using the LLM
                llm_explanation = fetch_llm(input=explain_swe_terms(input=term), model_name=model).get("data", {}).get("content", "")

                yield wf.stream_msg(msg={"title": f"LLM: explanation for '{term}'", "body": str(llm_explanation)})

                items_explained += 1

                # Update the original item in the list (find by original_index)
                for orig_item in input_file_content_transformed:
                    if orig_item["original_index"] == item["original_index"]:
                        orig_item["explanation"] = llm_explanation
                        break
        
        yield wf.stream_msg(msg={"title": f"Terms without explanation: {items_without_explanation}", "body": ""})

        yield wf.stream_msg(msg={"title": f"Terms explained: {items_explained}", "body": ""})

        if items_explained == 0:            
            return wf.success_response()

        # Transform the list of dictionaries into the required string format
        # Sort by original_index to maintain order
        input_file_content_transformed.sort(key=lambda x: x["original_index"])
        final_content = [
            f"{item['term']} == {item['explanation']}" if item.get('explanation') else f"{item['term']}"
            for item in input_file_content_transformed
        ]
        final_mixed_content = "\n\n-----\n\n".join(final_content)
        #print('final_mixed_content', final_mixed_content, sep="\n", end="\n\n")
        
        # Use Python's built-in file operations to overwrite the file completely
        output_file_path = Path(files_folder_root) / files_folder_path / (input_file_name + input_file_extension)
        
        # Validate the output path
        if not output_file_path:
            raise ValueError("Failed to construct output file path")
        
        # Ensure directory exists
        output_file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write the file in overwrite mode to replace all content
        output_file_path.write_text(final_mixed_content, encoding='utf-8')
        
        save_result = {
            ResponseKey.STATUS.value: ResponseStatus.SUCCESS.value,
            ResponseKey.MESSAGE.value: {
                ResponseKey.TITLE.value: "File saved (overwritten)",
                ResponseKey.BODY.value: f"File path: {output_file_path}"
            }
        }
        
        yield wf.stream_msg(msg=save_result["message"])

        return wf.success_response()

    except Exception as e:
        return wf.error_response(error=str(e))