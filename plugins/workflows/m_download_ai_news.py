from app.workflows import workflow, Workflow

@workflow()
def download_ai_news(task_id ): 
    """Downloads and saves recent AI-related news articles."""
    
    try:
        wf = Workflow(task_id=task_id)
        
        from user.tools import download_news_newsapi, split_clean, save_to_file, user_data_files_path, open_file
        import json                    

        open_file_result = open_file("ai_news.md")
        
        yield wf.stream_msg(msgTitle="Old articles - file", msgBody=open_file_result)

        old_articles = split_clean(open_file_result, delimiter="-----")

        old_articles_urls = [json.loads(article).get("url") for article in old_articles]

        # OR vs code OR hetzner OR open web ui OR hugging face
        news = download_news_newsapi(query="openai OR chatgpt OR mistral OR antrhopic OR claude OR github copilot OR cursor", lastDays=14, domains="techcrunch.com,thenextweb.com")
        if not news or not news.get("articles"):
            raise Exception("no news found")
        new_articles = news.get("articles", [])
        
        yield wf.stream_msg(msg={"title": f"New articles fetched ({len(new_articles)})", "body": str(new_articles)})

        new_articles_skipped = []
        new_articles_saved = []

        file_path = user_data_files_path("ai_news.md")
        db_file_path = user_data_files_path("databases/ai_news.json")

        for new_article in new_articles:
            if new_article.get("url") in old_articles_urls:                
                new_articles_skipped.append(new_article.get("url"))
                continue
            
            new_article_readable = json.dumps(new_article, indent=2, ensure_ascii=False)
            
            #json_db_add_entry(db_filepath=db_file_path, collection="entries", entry=article, add_createdat=False)
            
            save_file_result = save_to_file(filepath=file_path, content=new_article_readable, delimiter="-----", prepend=True)
            new_articles_saved.append(new_article.get("url"))
            

        yield wf.stream_msg(msgTitle=f"Skipped articles ({len(new_articles_skipped)})", msgBody=str(new_articles_skipped))
        
        yield wf.stream_msg(msgTitle=f"Saved articles ({len(new_articles_saved)})", msgBody=str(new_articles_saved))

        return wf.success_response()
    
    except Exception as e:
        return wf.error_response(error=e)
