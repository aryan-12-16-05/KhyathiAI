
from dataclasses import dataclass

from app.shared.youtube.models import TranscriptData


# ==========================================
# CHUNKING CONFIGURATION
# ==========================================

DEFAULT_MAX_WORDS = 1800


# ==========================================
# CHUNK DATA MODEL
# ==========================================

@dataclass(frozen=True, slots=True)
class TranscriptChunk:
    """Represents one timestamped transcript chunk."""

    chunk_id: int
    start_time: float
    end_time: float
    word_count: int
    text: str


# ==========================================
# WORD COUNT
# ==========================================

def count_words(text: str) -> int:
    """Returns the number of whitespace-separated words."""

    return len(text.split())


# ==========================================
# CHUNK CREATION
# ==========================================

def _create_chunk(
    chunk_id: int,
    snippets: list,
) -> TranscriptChunk:
    """Converts a group of transcript snippets into a chunk."""

    text = " ".join(
        snippet.text.strip()
        for snippet in snippets
    )

    start_time = min(
        snippet.start for snippet in snippets
    )

    end_time = max(
        snippet.start + snippet.duration
        for snippet in snippets
    )

    return TranscriptChunk(
        chunk_id=chunk_id,
        start_time=start_time,
        end_time=end_time,
        word_count=count_words(text),
        text=text,
    )


# ==========================================
# TRANSCRIPT CHUNKING
# ==========================================

def chunk_transcript(
    transcript: TranscriptData,
    max_words: int = DEFAULT_MAX_WORDS,
) -> tuple[TranscriptChunk, ...]:
    """
    Splits a cleaned transcript into timestamped chunks.

    Snippet boundaries are preserved whenever possible.

    If an individual caption snippet exceeds max_words,
    it is kept intact as a separate oversized chunk.
    This avoids inventing word-level timestamps.
    """

    if not isinstance(transcript, TranscriptData):
        raise TypeError(
            "Expected a TranscriptData instance."
        )

    if (
        not isinstance(max_words, int)
        or isinstance(max_words, bool)
        or max_words <= 0
    ):
        raise ValueError(
            "max_words must be a positive integer."
        )

    snippets = [
        snippet
        for snippet in transcript.snippets
        if snippet.text.strip()
    ]

    if not snippets:
        raise ValueError(
            "Transcript contains no usable snippets."
        )

    chunks = []
    current_snippets = []
    current_word_count = 0

    for snippet in snippets:

        snippet_word_count = count_words(snippet.text)

        # Skip empty snippets.
        if snippet_word_count == 0:
            continue

        # Handle a single oversized caption separately.
        if snippet_word_count > max_words:

            if current_snippets:
                chunks.append(
                    _create_chunk(
                        len(chunks) + 1,
                        current_snippets,
                    )
                )

                current_snippets = []
                current_word_count = 0

            chunks.append(
                _create_chunk(
                    len(chunks) + 1,
                    [snippet],
                )
            )

            continue

        # Start a new chunk when the word limit is exceeded.
        if (
            current_snippets
            and current_word_count + snippet_word_count > max_words
        ):
            chunks.append(
                _create_chunk(
                    len(chunks) + 1,
                    current_snippets,
                )
            )

            current_snippets = []
            current_word_count = 0

        current_snippets.append(snippet)
        current_word_count += snippet_word_count

    # Add the remaining snippets.
    if current_snippets:
        chunks.append(
            _create_chunk(
                len(chunks) + 1,
                current_snippets,
            )
        )

    return tuple(chunks)
