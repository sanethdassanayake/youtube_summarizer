import re
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
import google.generativeai as genai
from exceptions import *
from config import YOUTUBE_ID_REGEX, SUMMARY_PROMPT

def get_video_transcript(video_url: str) -> str:
    """Extract and return the transcript from a YouTube video URL."""
    if not video_url:
        raise InvalidURLError("No URL provided")
        
    try:
        match = re.search(YOUTUBE_ID_REGEX, video_url)
        if not match:
            raise InvalidURLError("Invalid YouTube video URL")
        
        video_id = match.group(1)
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([i['text'] for i in transcript])

    except TranscriptsDisabled:
        raise TranscriptsDisabledError("Transcripts are disabled for this video")
    except NoTranscriptFound:
        raise TranscriptNotFoundError("No transcript found for this video")
    except Exception as e:
        raise VideoError(f"An unexpected error occurred: {str(e)}")

def generate_summary(transcript: str) -> str:
    """Generate a structured summary using Gemini Pro."""
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(SUMMARY_PROMPT + "\n" + transcript)
        
        if response and response.candidates:
            return response.candidates[0].content.parts[0].text
        raise SummaryGenerationError("No summary could be generated")
        
    except Exception as e:
        raise SummaryGenerationError(f"Error generating summary: {str(e)}")

def process_video(url: str) -> tuple[str, str]:
    """Process video and return summary and error message."""
    try:
        transcript = get_video_transcript(url)
        summary = generate_summary(transcript)
        return summary, ""
    except VideoError as e:
        return "", str(e)
    except Exception as e:
        return "", f"An unexpected error occurred: {str(e)}"
