
import unittest

from types import SimpleNamespace

from youtube_transcript_api import NotTranslatable

from app.shared.youtube.transcript_service import TranscriptService
from app.shared.youtube.exceptions import (
    TranscriptUnavailableError,
)


VIDEO_ID = "ywaPnY_CBmk"


class FakeFetchedTranscript:

    def __init__(
        self,
        language="English",
        language_code="en",
        is_generated=False,
        text="Sample transcript",
    ):

        self.video_id = VIDEO_ID
        self.language = language
        self.language_code = language_code
        self.is_generated = is_generated

        self.snippets = [
            SimpleNamespace(
                text=text,
                start=0.0,
                duration=3.5,
            ),
            SimpleNamespace(
                text="Second segment",
                start=3.5,
                duration=2.5,
            ),
        ]

    def __iter__(self):
        return iter(self.snippets)


class FakeTrack:

    def __init__(
        self,
        language_code,
        is_generated=False,
        text="Sample transcript",
        translated_track=None,
    ):

        self.video_id = VIDEO_ID
        self.language_code = language_code
        self.language = language_code
        self.is_generated = is_generated
        self.text = text
        self.translated_track = translated_track

    def fetch(self):
        return FakeFetchedTranscript(
            language=self.language,
            language_code=self.language_code,
            is_generated=self.is_generated,
            text=self.text,
        )

    def translate(self, language_code):

        if self.translated_track is None:
            raise NotTranslatable(self.video_id)

        if language_code != "en":
            raise ValueError("Unexpected translation language")

        return self.translated_track


class FakeAPI:

    def __init__(self, tracks):
        self.tracks = tracks

    def list(self, video_id):
        return self.tracks


class TestTranscriptService(unittest.TestCase):

    def create_service(self, tracks):

        return TranscriptService(
            api_factory=lambda: FakeAPI(tracks)
        )

    def test_prefers_manual_english_transcript(self):

        generated = FakeTrack(
            language_code="en",
            is_generated=True,
            text="Generated captions",
        )

        manual = FakeTrack(
            language_code="en",
            is_generated=False,
            text="Manual captions",
        )

        service = self.create_service([manual, generated])

        result = service.fetch_transcript(VIDEO_ID)

        self.assertEqual(result.text.split()[0], "Manual")
        self.assertFalse(result.is_generated)
        self.assertFalse(result.was_translated)

    def test_uses_generated_english_when_manual_is_missing(self):

        generated = FakeTrack(
            language_code="en",
            is_generated=True,
        )

        service = self.create_service([generated])

        result = service.fetch_transcript(VIDEO_ID)

        self.assertEqual(result.language_code, "en")
        self.assertTrue(result.is_generated)

    def test_translates_non_english_transcript(self):

        translated = FakeTrack(
            language_code="en",
            is_generated=True,
            text="Translated English captions",
        )

        original = FakeTrack(
            language_code="fr",
            text="French captions",
            translated_track=translated,
        )

        service = self.create_service([original])

        result = service.fetch_transcript(VIDEO_ID)

        self.assertEqual(result.language_code, "en")
        self.assertTrue(result.was_translated)

    def test_falls_back_to_original_captions(self):

        original = FakeTrack(
            language_code="fr",
            text="Original French captions",
        )

        service = self.create_service([original])

        result = service.fetch_transcript(VIDEO_ID)

        self.assertEqual(result.language_code, "fr")
        self.assertFalse(result.was_translated)

    def test_missing_captions(self):

        service = self.create_service([])

        with self.assertRaises(TranscriptUnavailableError):
            service.fetch_transcript(VIDEO_ID)

    def test_rejects_invalid_video_id(self):

        service = self.create_service([])

        with self.assertRaises(ValueError):
            service.fetch_transcript("invalid")


if __name__ == "__main__":
    unittest.main()
