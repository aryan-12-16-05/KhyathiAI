
from pydantic import BaseModel, ConfigDict, HttpUrl


class SummarizationRequest(BaseModel):
    """
    Validated request received from the frontend
    when a user submits a YouTube video URL.
    """

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    youtube_url: HttpUrl
