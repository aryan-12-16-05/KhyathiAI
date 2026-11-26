
import unittest

from app.features.summarizer.schemas.response import (
    ChunkSummaryResponse,
    SummarizationResponse,
)


class TestResponseFormatting(unittest.TestCase):

    def test_duration_is_rounded_to_two_decimal_places(self):

        response = SummarizationResponse(
            video_id="ywaPnY_CBmk",
            language="English",
            language_code="en",
            is_generated=True,
            was_translated=False,
            duration_seconds=57.879000000000005,
            transcript_word_count=135,
            chunk_count=1,
            chunk_summaries=[
                ChunkSummaryResponse(
                    chunk_id=1,
                    start_time=2.2399999999999998,
                    end_time=57.879000000000005,
                    word_count=135,
                    summary="Sample chunk summary.",
                )
            ],
            final_summary="# Overall Summary\n\nSample summary.",
        )

        payload = response.model_dump(mode="json")

        self.assertEqual(
            payload["duration_seconds"],
            57.88,
        )

    def test_chunk_timestamps_are_rounded(self):

        chunk = ChunkSummaryResponse(
            chunk_id=1,
            start_time=2.2399999999999998,
            end_time=57.879000000000005,
            word_count=135,
            summary="Sample chunk summary.",
        )

        payload = chunk.model_dump(mode="json")

        self.assertEqual(payload["start_time"], 2.24)
        self.assertEqual(payload["end_time"], 57.88)

    def test_response_retains_all_summary_fields(self):

        response = SummarizationResponse(
            video_id="ywaPnY_CBmk",
            language="English",
            language_code="en",
            is_generated=True,
            was_translated=False,
            duration_seconds=57.88,
            transcript_word_count=135,
            chunk_count=1,
            chunk_summaries=[
                ChunkSummaryResponse(
                    chunk_id=1,
                    start_time=2.24,
                    end_time=57.88,
                    word_count=135,
                    summary="Sample chunk summary.",
                )
            ],
            final_summary="# Overall Summary\n\nSample summary.",
        )

        payload = response.model_dump(mode="json")

        self.assertEqual(payload["video_id"], "ywaPnY_CBmk")
        self.assertEqual(payload["chunk_count"], 1)
        self.assertEqual(len(payload["chunk_summaries"]), 1)

        self.assertIn("final_summary", payload)
        self.assertIn("transcript_word_count", payload)


if __name__ == "__main__":
    unittest.main()
