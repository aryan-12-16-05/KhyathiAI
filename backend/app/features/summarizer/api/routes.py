
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.features.summarizer.dependencies import (
    get_summarization_pipeline,
)

from app.features.summarizer.pipeline.summarization_pipeline import (
    SummarizationPipeline,
)

from app.features.summarizer.schemas import (
    SummarizationRequest,
    ChunkSummaryResponse,
    SummarizationResponse,
)

from app.shared.ai.exceptions import (
    OpenRouterError,
    OpenRouterAuthenticationError,
    OpenRouterConfigurationError,
    OpenRouterConnectionError,
    OpenRouterProviderError,
    OpenRouterRateLimitError,
    OpenRouterResponseError,
    OpenRouterTimeoutError,
)

from app.shared.youtube.exceptions import (
    TranscriptProviderError,
    TranscriptRetrievalError,
    TranscriptUnavailableError,
)

from app.shared.youtube.youtube_url import (
    YouTubeURLValidationError,
)


router = APIRouter(
    prefix="/summarizer",
    tags=["Summarizer"],
)


@router.post(
    "/summarize",
    response_model=SummarizationResponse,
    status_code=status.HTTP_200_OK,
    summary="Summarize a YouTube video",
    description=(
        "Retrieves a YouTube transcript, processes it through "
        "the AI summarization pipeline, and returns a "
        "structured summary."
    ),
)
async def summarize_youtube_video(
    payload: SummarizationRequest,
    pipeline: Annotated[
        SummarizationPipeline,
        Depends(get_summarization_pipeline),
    ],
) -> SummarizationResponse:
    """
    Executes the complete YouTube summarization workflow.
    """

    try:

        result = await pipeline.run(
            str(payload.youtube_url)
        )

    except YouTubeURLValidationError:

        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid or unsupported YouTube URL.",
        )

    except TranscriptUnavailableError:

        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Captions are unavailable for this video.",
        )

    except TranscriptProviderError:

        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=(
                "YouTube is temporarily unable to provide "
                "the transcript. Please try again later."
            ),
        )

    except TranscriptRetrievalError:

        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Unable to retrieve the video transcript.",
        )

    except OpenRouterRateLimitError:

        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=(
                "The free AI model endpoint is rate-limited. "
                "Please try again later."
            ),
        )

    except OpenRouterTimeoutError:

        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="The AI service request timed out.",
        )

    except OpenRouterConnectionError:

        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to connect to the AI service.",
        )

    except (
        OpenRouterAuthenticationError,
        OpenRouterConfigurationError,
    ):

        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="The AI service is not configured correctly.",
        )

    except OpenRouterProviderError:

        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="The AI provider is temporarily unavailable.",
        )

    except OpenRouterResponseError:

        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="The AI provider returned an invalid response.",
        )

    except OpenRouterError:

        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="An AI service error occurred.",
        )

    # Convert our internal result models into
    # the public API response schema.

    return SummarizationResponse(
        video_id=result.video_id,
        language=result.language,
        language_code=result.language_code,
        is_generated=result.is_generated,
        was_translated=result.was_translated,
        duration_seconds=result.duration_seconds,
        transcript_word_count=result.transcript_word_count,
        chunk_count=result.chunk_count,

        chunk_summaries=[
            ChunkSummaryResponse(
                chunk_id=chunk.chunk_id,
                start_time=chunk.start_time,
                end_time=chunk.end_time,
                word_count=chunk.word_count,
                summary=chunk.summary,
            )
            for chunk in result.chunk_summaries
        ],

        final_summary=result.final_summary,
    )
