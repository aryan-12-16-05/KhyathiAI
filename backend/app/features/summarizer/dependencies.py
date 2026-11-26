
import httpx

from fastapi import Request

from app.core.config import settings

from app.shared.ai.openrouter_client import (
    OpenRouterClient,
)

from app.shared.youtube.transcript_service import (
    TranscriptService,
)

from app.features.summarizer.pipeline.summarization_pipeline import (
    SummarizationPipeline,
)

from app.features.summarizer.services.chunk_summarizer import (
    ChunkSummarizer,
)

from app.features.summarizer.services.summary_builder import (
    SummaryBuilder,
)


def get_summarization_pipeline(
    request: Request,
) -> SummarizationPipeline:
    """
    Creates the summarization pipeline using
    the shared application HTTP client.

    Service dependencies are assembled here rather
    than inside API route implementations.
    """

    http_client: httpx.AsyncClient | None = getattr(
        request.app.state,
        "http_client",
        None,
    )

    if http_client is None:
        raise RuntimeError(
            "The application HTTP client is not initialized."
        )

    ai_client = OpenRouterClient(
        http_client=http_client,
        app_settings=settings,
    )

    transcript_service = TranscriptService()

    chunk_summarizer = ChunkSummarizer(
        ai_client=ai_client,
        max_tokens=2048,
        temperature=0.2,
    )

    summary_builder = SummaryBuilder(
        ai_client=ai_client,
        max_tokens=4096,
        temperature=0.2,
    )

    return SummarizationPipeline(
        transcript_service=transcript_service,
        chunk_summarizer=chunk_summarizer,
        summary_builder=summary_builder,
    )
