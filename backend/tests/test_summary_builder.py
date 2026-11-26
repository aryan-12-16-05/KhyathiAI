
import unittest

from types import SimpleNamespace
from unittest.mock import AsyncMock

from app.features.summarizer.pipeline.chunker import (
    TranscriptChunk,
)

from app.features.summarizer.services.summary_builder import (
    SummaryBuilder,
)


class TestSummaryBuilder(unittest.IsolatedAsyncioTestCase):

    def setUp(self):

        self.chunks = [
            TranscriptChunk(
                chunk_id=1,
                start_time=0.0,
                end_time=30.0,
                word_count=8,
                text="Artificial intelligence involves learning.",
            ),
            TranscriptChunk(
                chunk_id=2,
                start_time=30.0,
                end_time=60.0,
                word_count=7,
                text="Machine learning identifies patterns.",
            ),
        ]

        self.chunk_summaries = [
            "The speaker introduces artificial intelligence.",
            "The speaker explains machine learning and patterns.",
        ]

        self.ai_client = SimpleNamespace(
            generate=AsyncMock(
                return_value=SimpleNamespace(
                    content="# Overall Summary\n\nAI involves learning."
                )
            )
        )

        self.builder = SummaryBuilder(
            ai_client=self.ai_client
        )

    async def test_successful_final_summary(self):

        result = await self.builder.build(
            self.chunks,
            self.chunk_summaries,
        )

        self.assertEqual(
            result,
            "# Overall Summary\n\nAI involves learning.",
        )

        self.ai_client.generate.assert_awaited_once()

    async def test_passes_all_summaries_to_ai_client(self):

        await self.builder.build(
            self.chunks,
            self.chunk_summaries,
        )

        messages = (
            self.ai_client.generate
            .await_args.kwargs["messages"]
        )

        user_content = messages[1]["content"]

        for summary in self.chunk_summaries:
            self.assertIn(summary, user_content)

    async def test_preserves_chunk_order(self):

        await self.builder.build(
            self.chunks,
            self.chunk_summaries,
        )

        messages = (
            self.ai_client.generate
            .await_args.kwargs["messages"]
        )

        content = messages[1]["content"]

        self.assertLess(
            content.index("CHUNK 1"),
            content.index("CHUNK 2"),
        )

    async def test_preserves_timestamp_metadata(self):

        await self.builder.build(
            self.chunks,
            self.chunk_summaries,
        )

        messages = (
            self.ai_client.generate
            .await_args.kwargs["messages"]
        )

        content = messages[1]["content"]

        self.assertIn("0.00s - 30.00s", content)
        self.assertIn("30.00s - 60.00s", content)

    async def test_uses_default_generation_parameters(self):

        await self.builder.build(
            self.chunks,
            self.chunk_summaries,
        )

        arguments = self.ai_client.generate.await_args.kwargs

        self.assertEqual(arguments["max_tokens"], 4096)
        self.assertEqual(arguments["temperature"], 0.2)

    async def test_supports_custom_generation_parameters(self):

        client = SimpleNamespace(
            generate=AsyncMock(
                return_value=SimpleNamespace(
                    content="Custom final summary."
                )
            )
        )

        builder = SummaryBuilder(
            ai_client=client,
            max_tokens=2048,
            temperature=0.1,
        )

        await builder.build(
            self.chunks,
            self.chunk_summaries,
        )

        arguments = client.generate.await_args.kwargs

        self.assertEqual(arguments["max_tokens"], 2048)
        self.assertEqual(arguments["temperature"], 0.1)

    async def test_rejects_mismatched_chunk_counts(self):

        with self.assertRaises(ValueError):

            await self.builder.build(
                self.chunks,
                ["Only one summary."],
            )

    async def test_rejects_empty_summaries(self):

        with self.assertRaises(ValueError):

            await self.builder.build(
                self.chunks,
                ["  ", "Valid summary."],
            )

    async def test_rejects_invalid_chunk_input(self):

        with self.assertRaises(TypeError):

            await self.builder.build(
                ["Invalid chunk"],
                ["Some summary."],
            )

    async def test_propagates_ai_client_errors(self):

        self.ai_client.generate.side_effect = RuntimeError(
            "AI service unavailable."
        )

        with self.assertRaises(RuntimeError):

            await self.builder.build(
                self.chunks,
                self.chunk_summaries,
            )

    async def test_rejects_invalid_token_limit(self):

        with self.assertRaises(ValueError):

            SummaryBuilder(
                ai_client=self.ai_client,
                max_tokens=0,
            )

    async def test_rejects_invalid_temperature(self):

        with self.assertRaises(ValueError):

            SummaryBuilder(
                ai_client=self.ai_client,
                temperature=3.0,
            )


if __name__ == "__main__":
    unittest.main()
