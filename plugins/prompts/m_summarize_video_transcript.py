from app.prompts import prompt, render_prompt_with_context

@prompt()
def summarize_video_transcript(*, input: str):
    """Creates chapter-based summary of video transcription."""
    _prompt = """Analyze the video transcript and create a structured summary following these steps:
1. Identify natural chapter breaks based on content shifts
2. Create logical chapters with clear titles
3. Summarize key points for each chapter
4. Format output as:
   Chapter 1: [Title]
   - Key point 1
   - Key point 2

   Chapter 2: [Title]
   - Key point 1
   - Key point 2
    
    Input:
    {{ input }}
    """

    return render_prompt_with_context(_prompt.strip(), locals())