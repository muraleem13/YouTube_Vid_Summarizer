import re
from app.logger.logger import logger
logger = logger(__name__)

def extract_video_id(url):
    """
    Extract youtube vidoe ID from a given URL.
    This function uses a regular expression to match the video ID in various YouTube URL formats.
    :param url: Complete url of the YouTube video.
    :type url: str
    :raises ValueError: If the URL does not match any known YouTube formats.
    :example: https://www.youtube.com/watch?v=VIDEO_ID
    :return: Extracted video ID.
    :rtype: str
    """
    
    logger.info("Extracting video ID from URL: %s", url)
    youtube_pattern = r'(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})'
    
    logger.debug("Using regex pattern: %s", youtube_pattern)
    match = re.search(youtube_pattern, url)
    if match:
        logger.info("Video ID extracted successfully: %s", match.group(1))
        return match.group(1)
    else:
        logger.error("Failed to extract video ID from URL: %s", url)
        raise ValueError("Could not extract video ID from URL. Please check the URL format.")