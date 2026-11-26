
import { useCallback, useState } from "react";

import { summarizeYouTubeVideo } from "../services/summarizerApi";

import type { SummarizationResponse } from "../types";

interface UseSummarizerReturn {
    result: SummarizationResponse | null;
    isLoading: boolean;
    error: string | null;
    summarize: (youtubeUrl: string) => Promise<void>;
    reset: () => void;
}

export function useSummarizer(): UseSummarizerReturn {
    const [result, setResult] = useState<SummarizationResponse | null>(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const reset = useCallback(() => {
        setResult(null);
        setError(null);
        setIsLoading(false);
    }, []);

    const summarize = useCallback(async (youtubeUrl: string) => {
        setIsLoading(true);
        setError(null);
        setResult(null);

        try {
            const response = await summarizeYouTubeVideo(youtubeUrl);

            setResult(response);
        } catch (requestError: unknown) {
            const message =
                requestError instanceof Error
                    ? requestError.message
                    : "An unexpected error occurred. Please try again.";

            setError(message);
        } finally {
            setIsLoading(false);
        }
    }, []);

    return {
        result,
        isLoading,
        error,
        summarize,
        reset,
    };
}
