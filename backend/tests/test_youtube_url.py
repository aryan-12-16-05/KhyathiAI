
import unittest

from app.shared.youtube.youtube_url import (
    extract_video_id,
    YouTubeURLValidationError,
)


class TestYouTubeURLExtraction(unittest.TestCase):

    VIDEO_ID = "ywaPnY_CBmk"

    def test_standard_watch_url(self):
        url = f"https://www.youtube.com/watch?v={self.VIDEO_ID}"

        self.assertEqual(
            extract_video_id(url),
            self.VIDEO_ID,
        )

    def test_shortened_url(self):
        url = f"https://youtu.be/{self.VIDEO_ID}?si=test"

        self.assertEqual(
            extract_video_id(url),
            self.VIDEO_ID,
        )

    def test_shorts_url(self):
        url = f"https://www.youtube.com/shorts/{self.VIDEO_ID}"

        self.assertEqual(
            extract_video_id(url),
            self.VIDEO_ID,
        )

    def test_embed_url(self):
        url = f"https://www.youtube.com/embed/{self.VIDEO_ID}"

        self.assertEqual(
            extract_video_id(url),
            self.VIDEO_ID,
        )

    def test_live_url(self):
        url = f"https://www.youtube.com/live/{self.VIDEO_ID}"

        self.assertEqual(
            extract_video_id(url),
            self.VIDEO_ID,
        )

    def test_legacy_v_url(self):
        url = f"https://www.youtube.com/v/{self.VIDEO_ID}"

        self.assertEqual(
            extract_video_id(url),
            self.VIDEO_ID,
        )

    def test_mobile_youtube_url(self):
        url = f"https://m.youtube.com/watch?v={self.VIDEO_ID}"

        self.assertEqual(
            extract_video_id(url),
            self.VIDEO_ID,
        )

    def test_invalid_domain(self):
        with self.assertRaises(YouTubeURLValidationError):
            extract_video_id("https://example.com/watch?v=ywaPnY_CBmk")

    def test_missing_video_id(self):
        with self.assertRaises(YouTubeURLValidationError):
            extract_video_id("https://www.youtube.com/watch")

    def test_invalid_video_id_length(self):
        with self.assertRaises(YouTubeURLValidationError):
            extract_video_id("https://youtu.be/invalid")

    def test_empty_url(self):
        with self.assertRaises(YouTubeURLValidationError):
            extract_video_id("")

    def test_invalid_url_scheme(self):
        with self.assertRaises(YouTubeURLValidationError):
            extract_video_id("ftp://youtu.be/ywaPnY_CBmk")


if __name__ == "__main__":
    unittest.main()
