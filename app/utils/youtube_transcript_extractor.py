from youtube_transcript_api import YouTubeTranscriptApi
from app.logger.logger import logger
logger = logger(__name__)


def extract_transcript(video_id, language='en'):
    
    """
    Extracts the transcript of a YouTube video using its video ID.
    The transcript is returned as a single string, with all text concatenated together.
    If the transcript is not available in the specified language, an error message is logged and None is returned.
    param video_id: The ID of the YouTube video.
    type video_id: str
    param language: The language code for the transcript (default is 'en' for English).
    type language: str
    rturn: The transcript of the video as a single string, or None if not available.
    rtype: str or None
    """

    try:

        logger.info("Extracting transcript for video ID: %s", video_id)
        logger.debug("Using language: %s", language)

        transcript_content = YouTubeTranscriptApi.get_transcript(video_id=video_id, languages=[language])
        
        transcript = ' '.join([i['text'] for i in transcript_content])
        
        logger.info("Transcript extracted successfully")

        return transcript
    
    except Exception as e:

        logger.error("Error extracting transcript: %s", str(e))
        logger.debug("No transcript available for this video or language")

        return None