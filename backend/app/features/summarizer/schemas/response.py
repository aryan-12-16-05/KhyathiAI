
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_serializer,
)


class ChunkSummaryResponse(BaseModel):
    """Response representation of one summarized chunk."""

    model_config = ConfigDict(frozen=True)

    chunk_id: int = Field(ge=1)
    start_time: float = Field(ge=0)
    end_time: float = Field(ge=0)
    word_count: int = Field(ge=0)
    summary: str = Field(min_length=1)

    @field_serializer("start_time", "end_time")
    def serialize_timestamps(self, value: float) -> float:
        """Rounds serialized timestamps to two decimal places."""

        return round(value, 2)


class SummarizationResponse(BaseModel):
    """Complete response returned after video summarization."""

    model_config = ConfigDict(frozen=True)

    video_id: str
    language: str
    language_code: str
    is_generated: bool
    was_translated: bool

    duration_seconds: float = Field(ge=0)
    transcript_word_count: int = Field(ge=0)
    chunk_count: int = Field(ge=1)

    chunk_summaries: list[ChunkSummaryResponse]

    final_summary: str = Field(min_length=1)

    @field_serializer("duration_seconds")
    def serialize_duration(self, value: float) -> float:
        """Rounds serialized video duration to two decimal places."""

        return round(value, 2)
