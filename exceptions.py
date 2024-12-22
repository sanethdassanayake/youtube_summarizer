class VideoError(Exception):
    """Base exception for video processing errors"""
    pass

class InvalidURLError(VideoError):
    pass

class TranscriptsDisabledError(VideoError):
    pass

class TranscriptNotFoundError(VideoError):
    pass

class SummaryGenerationError(VideoError):
    pass 