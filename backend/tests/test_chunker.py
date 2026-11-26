
import unittest

from app.shared.youtube.models import (
    TranscriptData,
    TranscriptSnippet,
)

from app.features.summarizer.pipeline.chunker import (
    DEFAULT_MAX_WORDS,
    chunk_transcript,
)


class TestTranscriptChunker(unittest.TestCase):

    def create_transcript(self, snippets):

        return TranscriptData(
            video_id="ywaPnY_CBmk",
            language="English",
            language_code="en",
            is_generated=True,
            was_translated=False,
            snippets=tuple(snippets),
        )

    def test_default_word_limit(self):

        self.assertEqual(DEFAULT_MAX_WORDS, 1800)

    def test_splits_transcript_at_word_limit(self):

        transcript = self.create_transcript([
            TranscriptSnippet("One two", 0.0, 2.0),
            TranscriptSnippet("Three four", 2.0, 2.0),
            TranscriptSnippet("Five six", 4.0, 1.0),
        ])

        chunks = chunk_transcript(
            transcript,
            max_words=4,
        )

        self.assertEqual(len(chunks), 2)

        self.assertEqual(chunks[0].text, "One two Three four")
        self.assertEqual(chunks[0].word_count, 4)

        self.assertEqual(chunks[1].text, "Five six")
        self.assertEqual(chunks[1].word_count, 2)

    def test_preserves_timestamps(self):

        transcript = self.create_transcript([
            TranscriptSnippet("First sentence", 5.0, 3.0),
            TranscriptSnippet("Second sentence", 8.0, 2.0),
        ])

        chunks = chunk_transcript(
            transcript,
            max_words=10,
        )

        self.assertEqual(len(chunks), 1)
        self.assertEqual(chunks[0].start_time, 5.0)
        self.assertEqual(chunks[0].end_time, 10.0)

    def test_assigns_sequential_chunk_ids(self):

        transcript = self.create_transcript([
            TranscriptSnippet("One two", 0.0, 1.0),
            TranscriptSnippet("Three four", 2.0, 1.0),
            TranscriptSnippet("Five six", 4.0, 1.0),
        ])

        chunks = chunk_transcript(
            transcript,
            max_words=2,
        )

        self.assertEqual(
            [chunk.chunk_id for chunk in chunks],
            [1, 2, 3],
        )

    def test_supports_custom_word_limit(self):

        transcript = self.create_transcript([
            TranscriptSnippet("One two", 0.0, 1.0),
            TranscriptSnippet("Three four", 1.0, 1.0),
            TranscriptSnippet("Five six", 2.0, 1.0),
        ])

        chunks = chunk_transcript(
            transcript,
            max_words=3,
        )

        self.assertEqual(len(chunks), 3)

    def test_keeps_oversized_snippet_intact(self):

        transcript = self.create_transcript([
            TranscriptSnippet(
                "One two three four five",
                0.0,
                3.0,
            ),
            TranscriptSnippet("Six", 3.0, 1.0),
        ])

        chunks = chunk_transcript(
            transcript,
            max_words=3,
        )

        self.assertEqual(len(chunks), 2)
        self.assertEqual(chunks[0].word_count, 5)
        self.assertEqual(chunks[1].word_count, 1)

    def test_rejects_invalid_word_limit(self):

        transcript = self.create_transcript([
            TranscriptSnippet("Useful content", 0.0, 1.0),
        ])

        for invalid_limit in (0, -1, 1.5, True):

            with self.subTest(limit=invalid_limit):
                with self.assertRaises(ValueError):
                    chunk_transcript(
                        transcript,
                        max_words=invalid_limit,
                    )

    def test_rejects_empty_transcript(self):

        transcript = self.create_transcript([])

        with self.assertRaises(ValueError):
            chunk_transcript(transcript)

    def test_rejects_invalid_transcript(self):

        with self.assertRaises(TypeError):
            chunk_transcript("Invalid transcript")


if __name__ == "__main__":
    unittest.main()
