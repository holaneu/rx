from app.workflows import workflow, Workflow

@workflow()
def tool_calling_test(task_id, input, model=None):
    """Let's LLM to choose a tool for further processing."""
    
    try:
        wf = Workflow(task_id=task_id)

        from plugins.tools.m_included import fetch_llm

        def search_gutenberg_books(search_terms):
            search_query = " ".join(search_terms)
            url = "https://gutendex.com/books"
            response = requests.get(url, params={"search": search_query})
            simplified_results = []
            for book in response.json().get("results", []):
                simplified_results.append({
                    "id": book.get("id"),
                    "title": book.get("title"),
                    "authors": book.get("authors")
                })
            return simplified_results

        tools = [
            {
                "type": "function",
                "function": {
                    "name": "search_academic_papers",
                    "description": "Search for academic papers on a given topic",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string"},
                            "field": {"type": "string"}
                        },
                        "required": ["query"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_latest_statistics",
                    "description": "Get latest statistics on a topic",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "topic": {"type": "string"},
                            "year": {"type": "integer"}
                        },
                        "required": ["topic"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "search_gutenberg_books",
                    "description": "Search for books in the Project Gutenberg library",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "search_terms": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of search terms to find books"
                            }
                        },
                        "required": ["search_terms"]
                    }
                }
            }
        ]

        TOOL_MAPPING = {
            "search_gutenberg_books": search_gutenberg_books
        }

        llm_data = fetch_llm(model_name=model, input=input.strip(), tools=tools) #.get("data", {}).get("content", "")
        
        yield wf.stream_msg(msgTitle=f"LLM: ", msgBody=str(llm_data))

        return wf.success_response()
    
    except Exception as e:
        return wf.error_response(error=str(e))