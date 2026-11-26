
/**
 * Request sent to the KhyathiAI summarization API.
 */
export interface SummarizationRequest {
    youtube_url: string;
}

/**
 * Represents one summarized transcript chunk.
 */
export interface ChunkSummaryResponse {
    chunk_id: number;
    start_time: number;
    end_time: number;
    word_count: number;
    summary: string;
}

/**
 * Complete response received from the summarization API.
 */
export interface SummarizationResponse {
    video_id: string;
    language: string;
    language_code: string;
    is_generated: boolean;
    was_translated: boolean;

    duration_seconds: number;
    transcript_word_count: number;
    chunk_count: number;

    chunk_summaries: ChunkSummaryResponse[];

    final_summary: string;
}
