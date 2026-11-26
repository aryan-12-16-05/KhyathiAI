
from collections.abc import Callable

from youtube_transcript_api import (
    YouTubeTranscriptApi,
    YouTubeTranscriptApiException,
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable,
    VideoUnplayable,
    AgeRestricted,
    IpBlocked,
    RequestBlocked,
    PoTokenRequired,
    YouTubeRequestFailed,
    CouldNotRetrieveTranscript,
    NotTranslatable,
    TranslationLanguageNotAvailable,
)

from app.shared.youtube.exceptions import (
    TranscriptRetrievalError,
    TranscriptUnavailableError,
    TranscriptProviderError,
)

from app.shared.youtube.models import (
    TranscriptData,
    TranscriptSnippet,
)

from app.shared.youtube.youtube_url import VIDEO_ID_PATTERN


class TranscriptService:
    """
    Retrieves YouTube transcripts independently of API routes.

    Language selection:
    1. Prefer manually created English captions.
    2. Otherwise use generated English captions.
    3. Otherwise attempt translation into English.
    4. If translation is unavailable, use original captions.

    A fresh API client is created for each retrieval.
    """

    TARGET_LANGUAGE = "en"

    def __init__(
        self,
        api_factory: Callable[[], YouTubeTranscriptApi] | None = None,
    ) -> None:

        self._api_factory = api_factory or YouTubeTranscriptApi

    @staticmethod
    def _is_english(language_code: str) -> bool:
        """Recognizes English language codes."""

        return language_code.lower().split("-")[0] == "en"

    @staticmethod
    def _build_result(
        fetched_transcript,
        was_translated: bool,
    ) -> TranscriptData:
        """Converts the library response into our standard model."""

        snippets = tuple(
            TranscriptSnippet(
                text=snippet.text,
                start=float(snippet.start),
                duration=float(snippet.duration),
            )
            for snippet in fetched_transcript
        )

        if not snippets:
            raise TranscriptUnavailableError(
                "The retrieved transcript contains no captions."
            )

        return TranscriptData(
            video_id=fetched_transcript.video_id,
            language=fetched_transcript.language,
            language_code=fetched_transcript.language_code,
            is_generated=fetched_transcript.is_generated,
            was_translated=was_translated,
            snippets=snippets,
        )

    def fetch_transcript(
        self,
        video_id: str,
    ) -> TranscriptData:
        """
        Retrieves captions for a validated YouTube video ID.
        """

        if (
            not isinstance(video_id, str)
            or not VIDEO_ID_PATTERN.fullmatch(video_id)
        ):
            raise ValueError(
                "A valid 11-character YouTube video ID is required."
            )

        try:
            # Create a separate client for this retrieval.
            api = self._api_factory()

            # Retrieve all available caption tracks.
            transcript_list = api.list(video_id)
            available_tracks = list(transcript_list)

            if not available_tracks:
                raise TranscriptUnavailableError(
                    "No captions are available for this video."
                )

            # --------------------------------------
            # STEP 1: Prefer English captions
            # --------------------------------------

            english_tracks = [
                track
                for track in available_tracks
                if self._is_english(track.language_code)
            ]

            if english_tracks:

                # Prefer manually created English captions.
                selected_track = next(
                    (
                        track
                        for track in english_tracks
                        if not track.is_generated
                    ),
                    english_tracks[0],
                )

                fetched = selected_track.fetch()

                return self._build_result(
                    fetched,
                    was_translated=False,
                )

            # --------------------------------------
            # STEP 2: Attempt English translation
            # --------------------------------------

            for source_track in available_tracks:

                try:
                    translated_track = source_track.translate(
                        self.TARGET_LANGUAGE
                    )

                except (
                    NotTranslatable,
                    TranslationLanguageNotAvailable,
                ):
                    continue

                fetched = translated_track.fetch()

                return self._build_result(
                    fetched,
                    was_translated=True,
                )

            # --------------------------------------
            # STEP 3: Fall back to original captions
            # --------------------------------------

            original_track = available_tracks[0]

            fetched = original_track.fetch()

            return self._build_result(
                fetched,
                was_translated=False,
            )

        except TranscriptRetrievalError:
            raise

        except (
            TranscriptsDisabled,
            NoTranscriptFound,
            VideoUnavailable,
            VideoUnplayable,
            AgeRestricted,
        ) as exc:

            raise TranscriptUnavailableError(
                "Captions are unavailable for this YouTube video."
            ) from exc

        except (
            IpBlocked,
            RequestBlocked,
            PoTokenRequired,
            YouTubeRequestFailed,
            CouldNotRetrieveTranscript,
        ) as exc:

            raise TranscriptProviderError(
                "YouTube could not provide the transcript at this time. "
                "Please try again later."
            ) from exc

        except YouTubeTranscriptApiException as exc:

            raise TranscriptRetrievalError(
                "An unexpected YouTube transcript error occurred."
            ) from exc
