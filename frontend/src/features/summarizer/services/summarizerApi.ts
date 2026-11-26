
import { apiClient } from "../../../services/api/axiosClient";

import { normalizeApiError } from "../../../services/api/apiErrorHandler";

import type {
    SummarizationRequest,
    SummarizationResponse,
} from "../types";


/**
 * Sends a YouTube URL to the KhyathiAI backend
 * and returns the generated structured summary.
 */
export async function summarizeYouTubeVideo(
    youtubeUrl: string,
): Promise<SummarizationResponse> {

    const normalizedUrl = youtubeUrl.trim();

    if (!normalizedUrl) {
        throw new Error("Please enter a YouTube video URL.");
    }

    const requestPayload: SummarizationRequest = {
        youtube_url: normalizedUrl,
    };

    try {
        const response = await apiClient.post<SummarizationResponse>(
            "/summarizer/summarize",
            requestPayload,
        );

        return response.data;

    } catch (error: unknown) {
        throw normalizeApiError(error);
    }
}
