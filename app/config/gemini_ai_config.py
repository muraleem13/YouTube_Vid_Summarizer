import google.generativeai as genai
from dotenv import load_dotenv
import os
from app.logger.logger import logger

logger = logger(__name__)
load_dotenv()

logger.info("Loading environment variables...")

def configure_genai():
    """Configure the Google Gemini AI API with the API key from environment variables.
       rturns True if the API key is set and the configuration is successful, otherwise raises an error.
       rturn type: bool"""

    api_key = os.getenv("GEMINI_API_KEY")

    logger.info("Configuring Google Gemini AI API...")  
    logger.info(f"API Key: {api_key}")

    if not api_key:
        raise ValueError("API key is not set in the environment variables.")
    if api_key:
        genai.configure(api_key=api_key)
        return "True"
    return "False"