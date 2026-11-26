
class TranscriptRetrievalError(Exception):
    """Base exception for transcript retrieval failures."""


class TranscriptUnavailableError(TranscriptRetrievalError):
    """Raised when usable captions are unavailable."""


class TranscriptProviderError(TranscriptRetrievalError):
    """Raised when YouTube prevents or fails transcript retrieval."""
