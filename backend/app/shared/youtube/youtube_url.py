

import re

from urllib.parse import parse_qs, urlsplit


# ==========================================
# SUPPORTED YOUTUBE DOMAINS
# ==========================================

SUPPORTED_YOUTUBE_HOSTS = {
    "youtube.com",
    "www.youtube.com",
    "m.youtube.com",
    "music.youtube.com",
    "youtu.be",
    "www.youtu.be",
    "youtube-nocookie.com",
    "www.youtube-nocookie.com",
}


# ==========================================
# VIDEO ID VALIDATION
# ==========================================

VIDEO_ID_PATTERN = re.compile(
    r"^[A-Za-z0-9_-]{11}$"
)


# ==========================================
# CUSTOM VALIDATION ERROR
# ==========================================

class YouTubeURLValidationError(ValueError):
    """Raised when a YouTube URL is invalid or unsupported."""


# ==========================================
# VIDEO ID EXTRACTION
# ==========================================

def extract_video_id(video_url: str) -> str:
    """
    Extracts and validates an 11-character YouTube
    video ID from supported YouTube URL formats.

    Supported formats:
    - youtube.com/watch?v=VIDEO_ID
    - youtu.be/VIDEO_ID
    - youtube.com/shorts/VIDEO_ID
    - youtube.com/embed/VIDEO_ID
    - youtube.com/live/VIDEO_ID
    - youtube.com/v/VIDEO_ID
    """

    if not isinstance(video_url, str):
        raise YouTubeURLValidationError(
            "A valid YouTube URL must be provided."
        )

    video_url = video_url.strip()

    if not video_url:
        raise YouTubeURLValidationError(
            "YouTube URL cannot be empty."
        )

    try:
        parsed_url = urlsplit(video_url)
    except ValueError as exc:
        raise YouTubeURLValidationError(
            "The provided URL is malformed."
        ) from exc

    # Validate URL scheme.
    if parsed_url.scheme.lower() not in {"http", "https"}:
        raise YouTubeURLValidationError(
            "Only HTTP and HTTPS YouTube URLs are supported."
        )

    # Validate hostname.
    hostname = (parsed_url.hostname or "").lower().rstrip(".")

    if hostname not in SUPPORTED_YOUTUBE_HOSTS:
        raise YouTubeURLValidationError(
            "The provided URL is not from a supported YouTube domain."
        )

    # Reject URLs containing embedded credentials.
    if parsed_url.username is not None or parsed_url.password is not None:
        raise YouTubeURLValidationError(
            "YouTube URLs containing credentials are not supported."
        )

    path_segments = [
        segment
        for segment in parsed_url.path.split("/")
        if segment
    ]

    video_id = None

    # --------------------------------------
    # Shortened YouTube URLs
    # --------------------------------------

    if hostname in {"youtu.be", "www.youtu.be"}:

        if path_segments:
            video_id = path_segments[0]

    # --------------------------------------
    # Standard YouTube URLs
    # --------------------------------------

    elif hostname in {
        "youtube.com",
        "www.youtube.com",
        "m.youtube.com",
        "music.youtube.com",
    }:

        if parsed_url.path.rstrip("/") == "/watch":

            query_parameters = parse_qs(
                parsed_url.query,
                keep_blank_values=True,
            )

            video_values = query_parameters.get("v", [])

            if len(video_values) == 1:
                video_id = video_values[0]

        elif (
            len(path_segments) >= 2
            and path_segments[0] in {
                "shorts",
                "embed",
                "live",
                "v",
            }
        ):

            video_id = path_segments[1]

    # --------------------------------------
    # Privacy-enhanced embed URLs
    # --------------------------------------

    elif hostname in {
        "youtube-nocookie.com",
        "www.youtube-nocookie.com",
    }:

        if (
            len(path_segments) >= 2
            and path_segments[0] == "embed"
        ):
            video_id = path_segments[1]

    # --------------------------------------
    # Final video ID validation
    # --------------------------------------

    if not video_id or not VIDEO_ID_PATTERN.fullmatch(video_id):

        raise YouTubeURLValidationError(
            "Unable to extract a valid YouTube video ID from the URL."
        )

    return video_id
