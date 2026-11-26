
import html
import re

from app.shared.youtube.models import (
    TranscriptData,
    TranscriptSnippet,
)


# ==========================================
# TEXT CLEANING PATTERNS
# ==========================================

SPEAKER_MARKER_PATTERN = re.compile(r"^\s*>>\s*")

WHITESPACE_PATTERN = re.compile(r"\s+")


# ==========================================
# TRANSCRIPT CLEANER
# ==========================================

class TranscriptCleaner:
    """
    Cleans transcript text while preserving its
    original timestamps and metadata.
    """

    @staticmethod
    def clean_snippet(text: str) -> str:
        """
        Cleans an individual transcript snippet.
        """

        if not isinstance(text, str):
            raise TypeError("Transcript snippet must be a string.")

        # Decode HTML entities.
        text = html.unescape(text)

        # Remove invisible formatting characters.
        text = text.replace("\u200b", "")
        text = text.replace("\ufeff", "")

        # Remove leading YouTube speaker marker.
        text = SPEAKER_MARKER_PATTERN.sub("", text)

        # Normalize whitespace.
        text = WHITESPACE_PATTERN.sub(" ", text)

        return text.strip()

    @classmethod
    def clean(cls, transcript: TranscriptData) -> TranscriptData:
        """
        Cleans an entire transcript and returns
        a new immutable TranscriptData object.
        """

        if not isinstance(transcript, TranscriptData):
            raise TypeError(
                "Expected a TranscriptData instance."
            )

        cleaned_snippets = []

        for snippet in transcript.snippets:

            cleaned_text = cls.clean_snippet(snippet.text)

            # Ignore empty caption segments.
            if not cleaned_text:
                continue

            cleaned_snippets.append(
                TranscriptSnippet(
                    text=cleaned_text,
                    start=snippet.start,
                    duration=snippet.duration,
                )
            )

        if not cleaned_snippets:
            raise ValueError(
                "Transcript contains no usable text after cleaning."
            )

        return TranscriptData(
            video_id=transcript.video_id,
            language=transcript.language,
            language_code=transcript.language_code,
            is_generated=transcript.is_generated,
            was_translated=transcript.was_translated,
            snippets=tuple(cleaned_snippets),
        )
