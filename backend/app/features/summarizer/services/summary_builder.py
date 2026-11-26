
from collections.abc import Sequence

from app.features.summarizer.pipeline.chunker import (
    TranscriptChunk,
)

from app.features.summarizer.prompts import (
    build_final_summary_messages,
)

from app.shared.ai.openrouter_client import (
    OpenRouterClient,
)


# ==========================================
# FINAL SUMMARY BUILDER
# ==========================================

class SummaryBuilder:
    """
    Combines individual transcript chunk summaries
    into one comprehensive final summary.

    Responsibilities:
    - Accept all transcript chunks and their summaries.
    - Build the final consolidation prompt.
    - Communicate with the reusable OpenRouter client.
    - Return the final structured summary.
    """

    def __init__(
        self,
        ai_client: OpenRouterClient,
        max_tokens: int = 4096,
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

    async def build(
        self,
        chunks: Sequence[TranscriptChunk],
        chunk_summaries: Sequence[str],
    ) -> str:
        """
        Generates the final summary from all chunk summaries.
        """

        messages = build_final_summary_messages(
            chunks=chunks,
            chunk_summaries=chunk_summaries,
        )

        completion = await self._ai_client.generate(
            messages=messages,
            max_tokens=self._max_tokens,
            temperature=self._temperature,
        )

        return completion.content
