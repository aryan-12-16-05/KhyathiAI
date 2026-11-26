
import unittest

from types import SimpleNamespace
from unittest.mock import AsyncMock

from app.features.summarizer.pipeline.chunker import (
    TranscriptChunk,
)

from app.features.summarizer.services.chunk_summarizer import (
    ChunkSummarizer,
)


class TestChunkSummarizer(unittest.IsolatedAsyncioTestCase):

    def setUp(self):

        self.chunk = TranscriptChunk(
            chunk_id=1,
            start_time=0.0,
            end_time=30.0,
            word_count=8,
            text=(
                "Artificial intelligence involves "
                "learning and pattern recognition."
            ),
        )

        self.ai_client = SimpleNamespace(
            generate=AsyncMock(
                return_value=SimpleNamespace(
                    content="AI involves learning and recognizing patterns."
                )
            )
        )

        self.summarizer = ChunkSummarizer(
            ai_client=self.ai_client
        )

    async def test_successful_chunk_summarization(self):

        result = await self.summarizer.summarize(
            self.chunk
        )

        self.assertEqual(
            result,
            "AI involves learning and recognizing patterns.",
        )

        self.ai_client.generate.assert_awaited_once()

    async def test_passes_generated_prompt_to_ai_client(self):

        await self.summarizer.summarize(
            self.chunk
        )

        call_arguments = self.ai_client.generate.await_args

        messages = call_arguments.kwargs["messages"]

        self.assertEqual(len(messages), 2)
        self.assertIn(
            self.chunk.text,
            messages[1]["content"],
        )

    async def test_uses_default_generation_parameters(self):

        await self.summarizer.summarize(
            self.chunk
        )

        call_arguments = self.ai_client.generate.await_args

        self.assertEqual(
            call_arguments.kwargs["max_tokens"],
            2048,
        )

        self.assertEqual(
            call_arguments.kwargs["temperature"],
            0.2,
        )

    async def test_supports_custom_generation_parameters(self):

        client = SimpleNamespace(
            generate=AsyncMock(
                return_value=SimpleNamespace(
                    content="Custom summary."
                )
            )
        )

        summarizer = ChunkSummarizer(
            ai_client=client,
            max_tokens=4096,
            temperature=0.1,
        )

        await summarizer.summarize(
            self.chunk
        )

        arguments = client.generate.await_args.kwargs

        self.assertEqual(arguments["max_tokens"], 4096)
        self.assertEqual(arguments["temperature"], 0.1)

    async def test_rejects_invalid_chunk(self):

        with self.assertRaises(TypeError):

            await self.summarizer.summarize(
                "Invalid chunk"
            )

    async def test_rejects_invalid_token_limit(self):

        with self.assertRaises(ValueError):

            ChunkSummarizer(
                ai_client=self.ai_client,
                max_tokens=0,
            )

    async def test_rejects_invalid_temperature(self):

        with self.assertRaises(ValueError):

            ChunkSummarizer(
                ai_client=self.ai_client,
                temperature=3.0,
            )

    async def test_propagates_ai_client_errors(self):

        self.ai_client.generate.side_effect = RuntimeError(
            "AI service unavailable"
        )

        with self.assertRaises(RuntimeError):

            await self.summarizer.summarize(
                self.chunk
            )


if __name__ == "__main__":
    unittest.main()
