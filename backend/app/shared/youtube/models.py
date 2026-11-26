
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TranscriptSnippet:
    """Represents one timestamped transcript segment."""

    text: str
    start: float
    duration: float


@dataclass(frozen=True, slots=True)
class TranscriptData:
    """Standardized transcript returned by the retrieval service."""

    video_id: str
    language: str
    language_code: str
    is_generated: bool
    was_translated: bool
    snippets: tuple[TranscriptSnippet, ...]

    @property
    def text(self) -> str:
        """Combines all transcript snippets into plain text."""

        return " ".join(
            snippet.text for snippet in self.snippets
        )

    @property
    def duration_seconds(self) -> float:
        """Calculates the last transcript timestamp."""

        return max(
            (
                snippet.start + snippet.duration
                for snippet in self.snippets
            ),
            default=0.0,
        )
