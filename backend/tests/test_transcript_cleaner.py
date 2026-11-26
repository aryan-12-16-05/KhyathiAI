
import unittest

from app.shared.youtube.models import (
    TranscriptData,
    TranscriptSnippet,
)

from app.shared.youtube.transcript_cleaner import (
    TranscriptCleaner,
)


class TestTranscriptCleaner(unittest.TestCase):

    def setUp(self):

        self.cleaner = TranscriptCleaner

        self.transcript = TranscriptData(
            video_id="ywaPnY_CBmk",
            language="English",
            language_code="en",
            is_generated=True,
            was_translated=False,
            snippets=(
                TranscriptSnippet(
                    text="  >> Hello    world!  ",
                    start=0.0,
                    duration=2.0,
                ),
                TranscriptSnippet(
                    text="Artificial &amp; Intelligence",
                    start=2.0,
                    duration=3.0,
                ),
            ),
        )

    def test_removes_speaker_marker(self):

        result = self.cleaner.clean_snippet(
            ">> Hello there!"
        )

        self.assertEqual(result, "Hello there!")

    def test_decodes_html_entities(self):

        result = self.cleaner.clean_snippet(
            "Artificial &amp; Intelligence"
        )

        self.assertEqual(
            result,
            "Artificial & Intelligence",
        )

    def test_normalizes_whitespace(self):

        result = self.cleaner.clean_snippet(
            "  Hello   \n world \t again  "
        )

        self.assertEqual(
            result,
            "Hello world again",
        )

    def test_removes_invisible_characters(self):

        result = self.cleaner.clean_snippet(
            "Hello\u200b Wor\ufeffld"
        )

        self.assertEqual(result, "Hello World")

    def test_preserves_timestamps_and_metadata(self):

        cleaned = self.cleaner.clean(self.transcript)

        self.assertEqual(cleaned.video_id, self.transcript.video_id)
        self.assertEqual(cleaned.language_code, "en")
        self.assertTrue(cleaned.is_generated)
        self.assertEqual(len(cleaned.snippets), 2)

        self.assertEqual(cleaned.snippets[0].start, 0.0)
        self.assertEqual(cleaned.snippets[0].duration, 2.0)

    def test_removes_empty_snippets(self):

        transcript = TranscriptData(
            video_id="ywaPnY_CBmk",
            language="English",
            language_code="en",
            is_generated=True,
            was_translated=False,
            snippets=(
                TranscriptSnippet(
                    text="   ",
                    start=0.0,
                    duration=1.0,
                ),
                TranscriptSnippet(
                    text="Useful content",
                    start=1.0,
                    duration=2.0,
                ),
            ),
        )

        cleaned = self.cleaner.clean(transcript)

        self.assertEqual(len(cleaned.snippets), 1)
        self.assertEqual(
            cleaned.snippets[0].text,
            "Useful content",
        )

    def test_rejects_completely_empty_transcript(self):

        transcript = TranscriptData(
            video_id="ywaPnY_CBmk",
            language="English",
            language_code="en",
            is_generated=True,
            was_translated=False,
            snippets=(
                TranscriptSnippet(
                    text="   ",
                    start=0.0,
                    duration=1.0,
                ),
            ),
        )

        with self.assertRaises(ValueError):
            self.cleaner.clean(transcript)

    def test_rejects_invalid_input(self):

        with self.assertRaises(TypeError):
            self.cleaner.clean("Not a transcript")


if __name__ == "__main__":
    unittest.main()
