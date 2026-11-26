
const YOUTUBE_HOSTS = new Set([
    "youtube.com",
    "www.youtube.com",
    "m.youtube.com",
    "music.youtube.com",
    "youtu.be",
    "www.youtu.be",
    "youtube-nocookie.com",
    "www.youtube-nocookie.com",
]);

const VIDEO_ID_PATTERN = /^[A-Za-z0-9_-]{11}$/;

/**
 * Validates a supported YouTube URL before submitting it.
 *
 * Backend validation remains the final authority.
 */
export function validateYouTubeUrl(value: string): string | null {
    const trimmedValue = value.trim();

    if (!trimmedValue) {
        return "Please enter a YouTube video URL.";
    }

    let parsedUrl: URL;

    try {
        parsedUrl = new URL(trimmedValue);
    } catch {
        return "Please enter a valid URL.";
    }

    if (!["http:", "https:"].includes(parsedUrl.protocol)) {
        return "Only HTTP and HTTPS URLs are supported.";
    }

    if (parsedUrl.username || parsedUrl.password) {
        return "URLs containing credentials are not supported.";
    }

    const hostname = parsedUrl.hostname.toLowerCase().replace(/\.$/, "");

    if (!YOUTUBE_HOSTS.has(hostname)) {
        return "Please enter a supported YouTube URL.";
    }

    const segments = parsedUrl.pathname
        .split("/")
        .filter(Boolean);

    let videoId: string | null = null;

    if (["youtu.be", "www.youtu.be"].includes(hostname)) {
        videoId = segments[0] ?? null;
    } else if (
        ["youtube-nocookie.com", "www.youtube-nocookie.com"].includes(hostname)
    ) {
        if (segments[0] === "embed") {
            videoId = segments[1] ?? null;
        }
    } else if (parsedUrl.pathname.replace(/\/+$/, "") === "/watch") {
        const values = parsedUrl.searchParams.getAll("v");

        if (values.length === 1) {
            videoId = values[0];
        }
    } else if (
        ["shorts", "embed", "live", "v"].includes(segments[0] ?? "")
    ) {
        videoId = segments[1] ?? null;
    }

    if (!videoId || !VIDEO_ID_PATTERN.test(videoId)) {
        return "Unable to find a valid YouTube video ID in this URL.";
    }

    return null;
}
