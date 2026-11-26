
import unittest

from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock

from app.shared.youtube.models import (
    TranscriptData,
    TranscriptSnippet,
)

from app.shared.youtube.youtube_url import (
    YouTubeURLValidationError,
)

from app.features.summarizer.pipeline.summarization_pipeline import (
    SummarizationPipeline,
)


VIDEO_URL = "https://youtu.be/ywaPnY_CBmk"
VIDEO_ID = "ywaPnY_CBmk"


class TestSummarizationPipeline(unittest.IsolatedAsyncioTestCase):

    def setUp(self):

        self.transcript = TranscriptData(
            video_id=VIDEO_ID,
            language="English",
            language_code="en",
            is_generated=True,
            was_translated=False,
            snippets=(
                TranscriptSnippet(
                    text="Artificial intelligence involves learning.",
                    start=0.0,
                    duration=2.0,
                ),
                TranscriptSnippet(
                    text="Machine learning identifies patterns.",
                    start=2.0,
                    duration=2.0,
                ),
            ),
        )

        self.transcript_service = SimpleNamespace(
            fetch_transcript=Mock(
                return_value=self.transcript
            )
        )

        self.chunk_summarizer = SimpleNamespace(
            summarize=AsyncMock(
                side_effect=[
                    "First chunk summary.",
                    "Second chunk summary.",
                ]
            )
        )

        self.summary_builder = SimpleNamespace(
            build=AsyncMock(
                return_value="# Final Summary\n\nComplete summary."
            )
        )

        self.pipeline = SummarizationPipeline(
            transcript_service=self.transcript_service,
            chunk_summarizer=self.chunk_summarizer,
            summary_builder=self.summary_builder,
            max_words=5,
        )

    async def test_complete_pipeline_success(self):

        result = await self.pipeline.run(VIDEO_URL)

        self.assertEqual(result.video_id, VIDEO_ID)

        self.assertEqual(
            result.final_summary,
            "# Final Summary\n\nComplete summary.",
        )

        self.assertEqual(result.chunk_count, 2)

        self.assertEqual(
            result.chunk_summaries[0].summary,
            "First chunk summary.",
        )

        self.assertEqual(
            result.chunk_summaries[1].summary,
            "Second chunk summary.",
        )

    async def test_extracts_video_id_before_retrieval(self):

        await self.pipeline.run(VIDEO_URL)

        self.transcript_service.fetch_transcript.assert_called_once_with(
            VIDEO_ID
        )

    async def test_summarizes_every_chunk(self):

        await self.pipeline.run(VIDEO_URL)

        self.assertEqual(
            self.chunk_summarizer.summarize.await_count,
            2,
        )

    async def test_builds_final_summary_once(self):

        await self.pipeline.run(VIDEO_URL)

        self.summary_builder.build.assert_awaited_once()

    async def test_preserves_transcript_metadata(self):

        result = await self.pipeline.run(VIDEO_URL)

        self.assertEqual(result.language, "English")
        self.assertEqual(result.language_code, "en")
        self.assertTrue(result.is_generated)
        self.assertFalse(result.was_translated)
        self.assertEqual(result.duration_seconds, 4.0)
        self.assertEqual(result.transcript_word_count, 8)

    async def test_rejects_invalid_youtube_url(self):

        with self.assertRaises(YouTubeURLValidationError):

            await self.pipeline.run(
                "https://example.com/video"
            )

        self.transcript_service.fetch_transcript.assert_not_called()

    async def test_propagates_transcript_retrieval_failure(self):

        self.transcript_service.fetch_transcript.side_effect = (
            RuntimeError("Transcript retrieval failed.")
        )

        with self.assertRaises(RuntimeError):

            await self.pipeline.run(VIDEO_URL)

        self.summary_builder.build.assert_not_awaited()

    async def test_stops_when_chunk_summarization_fails(self):

        self.chunk_summarizer.summarize.side_effect = RuntimeError(
            "AI summarization failed."
        )

        with self.assertRaises(RuntimeError):

            await self.pipeline.run(VIDEO_URL)

        self.summary_builder.build.assert_not_awaited()

    async def test_propagates_final_summary_failure(self):

        self.summary_builder.build.side_effect = RuntimeError(
            "Final summary generation failed."
        )

        with self.assertRaises(RuntimeError):

            await self.pipeline.run(VIDEO_URL)

    async def test_rejects_invalid_chunk_limit(self):

        with self.assertRaises(ValueError):

            SummarizationPipeline(
                transcript_service=self.transcript_service,
                chunk_summarizer=self.chunk_summarizer,
                summary_builder=self.summary_builder,
                max_words=0,
            )


if __name__ == "__main__":
    unittest.main()
