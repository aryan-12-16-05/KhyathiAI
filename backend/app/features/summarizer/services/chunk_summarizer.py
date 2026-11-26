
from app.features.summarizer.pipeline.chunker import (
    TranscriptChunk,
)

from app.features.summarizer.prompts import (
    build_chunk_summary_messages,
)

from app.shared.ai.openrouter_client import (
    OpenRouterClient,
)


# ==========================================
# CHUNK SUMMARIZER SERVICE
# ==========================================

class ChunkSummarizer:
    """
    Generates an AI summary for an individual transcript chunk.

    Responsibilities:
    - Build the chunk-specific prompt.
    - Communicate with the reusable OpenRouter client.
    - Return the generated summary.

    API communication and prompt construction remain
    delegated to their respective modules.
    """

    def __init__(
        self,
        ai_client: OpenRouterClient,
        max_tokens: int = 2048,
        temperature: float = 0.2,
    ) -> None:

        if (
            not isinstance(max_tokens, int)
            or isinstance(max_tokens, bool)
            or max_tokens <= 0
        ):
            raise ValueError(
                "max_tokens must be a positive integer."
            )

        if (
            not isinstance(temperature, (int, float))
            or isinstance(temperature, bool)
            or not 0 <= temperature <= 2
        ):
            raise ValueError(
                "temperature must be between 0 and 2."
            )

        self._ai_client = ai_client
        self._max_tokens = max_tokens
        self._temperature = temperature

    async def summarize(
        self,
        chunk: TranscriptChunk,
    ) -> str:
        """
        Summarizes one transcript chunk using the configured AI model.
        """

        if not isinstance(chunk, TranscriptChunk):
            raise TypeError(
                "Expected a TranscriptChunk instance."
            )

        messages = build_chunk_summary_messages(chunk)

        completion = await self._ai_client.generate(
            messages=messages,
            max_tokens=self._max_tokens,
            temperature=self._temperature,
        )

        return completion.content
