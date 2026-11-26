
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ChunkSummaryResult:
    """Stores one summarized transcript chunk."""

    chunk_id: int
    start_time: float
    end_time: float
    word_count: int
    summary: str


@dataclass(frozen=True, slots=True)
class SummarizationResult:
    """Stores the complete YouTube summarization result."""

    video_id: str
    language: str
    language_code: str
    is_generated: bool
    was_translated: bool
    duration_seconds: float
    transcript_word_count: int
    chunk_count: int
    chunk_summaries: tuple[ChunkSummaryResult, ...]
    final_summary: str
