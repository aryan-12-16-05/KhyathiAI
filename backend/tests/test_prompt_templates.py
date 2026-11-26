
import unittest

from app.features.summarizer.pipeline.chunker import (
    TranscriptChunk,
)

from app.features.summarizer.prompts import (
    build_chunk_summary_messages,
    build_final_summary_messages,
)


class TestPromptTemplates(unittest.TestCase):

    def setUp(self):

        self.chunk_one = TranscriptChunk(
            chunk_id=1,
            start_time=0.0,
            end_time=30.0,
            word_count=5,
            text="Artificial intelligence involves learning.",
        )

        self.chunk_two = TranscriptChunk(
            chunk_id=2,
            start_time=30.0,
            end_time=60.0,
            word_count=5,
            text="Machine learning identifies patterns.",
        )

    # ======================================
    # CHUNK PROMPT TESTS
    # ======================================

    def test_chunk_prompt_returns_system_and_user_messages(self):

        messages = build_chunk_summary_messages(
            self.chunk_one
        )

        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0]["role"], "system")
        self.assertEqual(messages[1]["role"], "user")

    def test_chunk_prompt_contains_transcript(self):

        messages = build_chunk_summary_messages(
            self.chunk_one
        )

        self.assertIn(
            self.chunk_one.text,
            messages[1]["content"],
        )

    def test_chunk_prompt_contains_timestamp_metadata(self):

        messages = build_chunk_summary_messages(
            self.chunk_one
        )

        self.assertIn("0.00 seconds", messages[1]["content"])
        self.assertIn("30.00 seconds", messages[1]["content"])

    def test_chunk_prompt_rejects_empty_text(self):

        empty_chunk = TranscriptChunk(
            chunk_id=1,
            start_time=0.0,
            end_time=10.0,
            word_count=0,
            text="",
        )

        with self.assertRaises(ValueError):
            build_chunk_summary_messages(empty_chunk)

    def test_chunk_prompt_rejects_invalid_input(self):

        with self.assertRaises(TypeError):
            build_chunk_summary_messages("invalid")

    def test_chunk_prompt_preserves_speaker_attribution_rules(self):

        messages = build_chunk_summary_messages(
            self.chunk_one
        )

        system_prompt = messages[0]["content"]
        normalized_prompt = " ".join(system_prompt.split())

        self.assertIn(
             "Never invent facts, examples, explanations, or conclusions.",
            normalized_prompt,
        )

        self.assertIn(
            "explicitly attribute it to the speaker",
            normalized_prompt,
        )

    # ======================================
    # FINAL SUMMARY PROMPT TESTS
    # ======================================

    def test_final_prompt_combines_chunk_summaries(self):

        summaries = [
            "The speaker introduces artificial intelligence.",
            "The speaker explains machine learning.",
        ]

        messages = build_final_summary_messages(
            [self.chunk_one, self.chunk_two],
            summaries,
        )

        self.assertEqual(len(messages), 2)
        self.assertIn(summaries[0], messages[1]["content"])
        self.assertIn(summaries[1], messages[1]["content"])

    def test_final_prompt_preserves_chunk_order_and_timestamps(self):

        messages = build_final_summary_messages(
            [self.chunk_one, self.chunk_two],
            ["First summary.", "Second summary."],
        )

        content = messages[1]["content"]

        self.assertLess(
            content.index("CHUNK 1"),
            content.index("CHUNK 2"),
        )

        self.assertIn("0.00s - 30.00s", content)
        self.assertIn("30.00s - 60.00s", content)

    def test_final_prompt_rejects_mismatched_counts(self):

        with self.assertRaises(ValueError):
            build_final_summary_messages(
                [self.chunk_one, self.chunk_two],
                ["Only one summary."],
            )

    def test_final_prompt_rejects_empty_summaries(self):

        with self.assertRaises(ValueError):
            build_final_summary_messages(
                [self.chunk_one],
                ["   "],
            )

    def test_final_prompt_rejects_empty_input(self):

        with self.assertRaises(ValueError):
            build_final_summary_messages([], [])

    def test_final_prompt_rejects_invalid_chunk(self):

        with self.assertRaises(TypeError):
            build_final_summary_messages(
                ["invalid"],
                ["Some summary."],
            )


    def test_chunk_prompt_prevents_ai_ml_equivalence(self):

        messages = build_chunk_summary_messages(
            self.chunk_one
        )

        system_prompt = messages[0]["content"]

        self.assertIn(
            "Never present artificial intelligence and machine learning",
            system_prompt,
        )

    def test_final_prompt_preserves_speaker_attribution(self):

        messages = build_final_summary_messages(
            [self.chunk_one],
            ["The speaker presents AI as machine learning."],
        )

        system_prompt = messages[0]["content"]

        self.assertIn(
            "Never convert a simplified speaker explanation",
            system_prompt,
        )

    def test_final_prompt_prevents_unsupported_timestamps(self):

        messages = build_final_summary_messages(
            [self.chunk_one],
            ["The speaker discusses artificial intelligence."],
        )

        system_prompt = messages[0]["content"]

        self.assertIn(
            "Do not invent precise topic timestamps",
            system_prompt,
        )

if __name__ == "__main__":
    unittest.main()
