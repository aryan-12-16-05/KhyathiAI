
import type { SummarizationResponse } from "../types";

import VideoMetadata from "./VideoMetadata";
import FinalSummary from "./FinalSummary";
import ChunkSummaryList from "./ChunkSummaryList";

import "./SummarizationResults.css";

interface SummarizationResultsProps {
    data: SummarizationResponse;
}

function SummarizationResults({
    data,
}: SummarizationResultsProps) {
    return (
        <section
            className="summarization-results"
            aria-label="YouTube summarization results"
        >
            <VideoMetadata data={data} />

            <FinalSummary summary={data.final_summary} />

            {data.chunk_summaries.length > 0 && (
                <ChunkSummaryList chunks={data.chunk_summaries} />
            )}
        </section>
    );
}

export default SummarizationResults;
