from app.config.gemini_ai_config import configure_genai
import google.generativeai as genai
from dotenv import load_dotenv
from app.logger.logger import logger
logger = logger(__name__)


def generate_markdown_summary(transcript_text, video_id=None):
    """
    Generate a well-formatted Markdown summary of a YouTube video transcript using Google Gemini AI.
    Args: transcript_text (str): The transcript text of the YouTube video.
          video_id (str): The YouTube video ID (optional).
          Returns: str: A Markdown formatted summary of the video transcript.
          """

    try:

        if not configure_genai():
            logger.error("Gemini AI API key is not set in the environment variables.")
            raise ValueError("Gemini AI API key is not set in the environment variables.")

        model = genai.GenerativeModel(model_name='gemini-2.0-flash')
        logger.info("Gemini AI model initialized successfully.")
        logger.info(f"Model name: {model.model_name}")
        
        video_info = f"Video: {video_id}\n\n" if video_id else ""
        
        prompt = f"""You are a YouTube video summarizer that creates well-formatted Markdown summaries.

Based on the transcript I'm providing, create a comprehensive summary (within 500 words) with the following:

1. Start with a level 1 heading (# ) for the main title that captures the essence of the content
2. Include a brief introduction paragraph
3. Organize key points under level 2 headings (## )
4. Use appropriate Markdown formatting:
   - Bullet points for lists
   - Bold text for emphasis
   - Blockquotes for notable quotes
   - Code blocks for technical content if relevant
   - Tables if comparing information is valuable

Here's the transcript to summarize:

{transcript_text}"""
        
        response = model.generate_content(prompt)
        
        markdown_summary = video_info + response.text

        logger.info(f"Generated summary for video {video_id}: {markdown_summary}")
        
        return markdown_summary
    
    except Exception as e:
        logger.error(f"Error generating summary: {e}")
        return None