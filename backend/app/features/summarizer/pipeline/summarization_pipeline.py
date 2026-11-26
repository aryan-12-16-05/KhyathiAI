
import asyncio

from app.shared.youtube.youtube_url import extract_video_id
from app.shared.youtube.transcript_service import TranscriptService
from app.shared.youtube.transcript_cleaner import TranscriptCleaner

from app.features.summarizer.pipeline.chunker import (
    DEFAULT_MAX_WORDS,
    TranscriptChunk,
    chunk_transcript,
    count_words,
)

from app.features.summarizer.pipeline.results import (
    ChunkSummaryResult,
    SummarizationResult,
)

from app.features.summarizer.services.chunk_summarizer import (
    ChunkSummarizer,
)

from app.features.summarizer.services.summary_builder import (
    SummaryBuilder,
)


class SummarizationPipeline:
    """
    Coordinates the complete YouTube summarization workflow.

    Workflow:
    1. Extract YouTube video ID.
    2. Retrieve transcript.
    3. Clean transcript.
    4. Divide transcript into chunks.
    5. Summarize individual chunks.
    6. Consolidate chunk summaries.
    7. Return a standardized result.

    Individual responsibilities remain delegated to
    their respective service modules.
    """

    def __init__(
        self,
        transcript_service: TranscriptService,
        chunk_summarizer: ChunkSummarizer,
        summary_builder: SummaryBuilder,
        max_words: int = DEFAULT_MAX_WORDS,
    ) -> None:

        if (
            not isinstance(max_words, int)
            or isinstance(max_words, bool)
            or max_words <= 0
        ):
            raise ValueError(
                "max_words must be a positive integer."
            )

        self._transcript_service = transcript_service
        self._chunk_summarizer = chunk_summarizer
        self._summary_builder = summary_builder
        self._max_words = max_words

    async def run(
        self,
        youtube_url: str,
    ) -> SummarizationResult:
        """
        Executes the complete YouTube summarization pipeline.
        """

        # ======================================
        # STEP 1: EXTRACT VIDEO ID
        # ======================================

        video_id = extract_video_id(youtube_url)

        # ======================================
        # STEP 2: RETRIEVE TRANSCRIPT
        # ======================================

        # Transcript retrieval is synchronous.
        # Run it in a worker thread to avoid blocking
        # the asynchronous FastAPI event loop.

        transcript = await asyncio.to_thread(
            self._transcript_service.fetch_transcript,
            video_id,
        )

        # ======================================
        # STEP 3: CLEAN TRANSCRIPT
        # ======================================

        cleaned_transcript = TranscriptCleaner.clean(
            transcript
        )

        # ======================================
        # STEP 4: CHUNK TRANSCRIPT
        # ======================================

        chunks = chunk_transcript(
            cleaned_transcript,
            max_words=self._max_words,
        )

        if not chunks:
            raise ValueError(
                "Transcript could not be divided into usable chunks."
            )

        # ======================================
        # STEP 5: SUMMARIZE EACH CHUNK
        # ======================================

        chunk_summaries = []

        # Sequential processing is intentional.
        # It keeps free-model request usage predictable.

        for chunk in chunks:

            summary = await self._chunk_summarizer.summarize(
                chunk
            )

            chunk_summaries.append(summary)

        # ======================================
        # STEP 6: BUILD FINAL SUMMARY
        # ======================================

        final_summary = await self._summary_builder.build(
            chunks=chunks,
            chunk_summaries=chunk_summaries,
        )

        # ======================================
        # STEP 7: BUILD STANDARDIZED RESULT
        # ======================================

        chunk_results = tuple(
            ChunkSummaryResult(
                chunk_id=chunk.chunk_id,
                start_time=chunk.start_time,
                end_time=chunk.end_time,
                word_count=chunk.word_count,
                summary=summary,
            )
            for chunk, summary in zip(
                chunks,
                chunk_summaries,
            )
        )

        return SummarizationResult(
            video_id=cleaned_transcript.video_id,
            language=cleaned_transcript.language,
            language_code=cleaned_transcript.language_code,
            is_generated=cleaned_transcript.is_generated,
            was_translated=cleaned_transcript.was_translated,
            duration_seconds=cleaned_transcript.duration_seconds,
            transcript_word_count=count_words(
                cleaned_transcript.text
            ),
            chunk_count=len(chunks),
            chunk_summaries=chunk_results,
            final_summary=final_summary,
        )
