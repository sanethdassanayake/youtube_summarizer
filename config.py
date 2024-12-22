import os
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai

# Constants
YOUTUBE_ID_REGEX = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
SUMMARY_PROMPT = """
You are an expert at summarizing YouTube videos. Your job is to analyze the video transcript and produce a detailed, informative, and concise summary. The summary should:

1. Capture all key points, insights, and arguments presented in the video.
2. Include relevant examples or explanations from the video (if applicable) to provide context.
3. Be written in simple and clear language, avoiding filler, repetition, or unnecessary details.
4. Present the main ideas logically and in the order they are discussed in the video.
5. Stay within a 300-word limit.

Format the summary in the following structure:
1. [Main point or insight with a brief explanation if needed]
2. [Next key idea or argument with context or example if necessary]
3. [Additional points or conclusions]
"""

def init_api():
    """Initialize API configuration"""
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment variables")
    genai.configure(api_key=api_key) 