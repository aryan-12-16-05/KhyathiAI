
import type { ChunkSummaryResponse } from "../types";

import { formatDuration } from "../utils/formatDuration";

import MarkdownRenderer from "./MarkdownRenderer";

import "./ChunkSummaryList.css";

interface ChunkSummaryListProps {
    chunks: ChunkSummaryResponse[];
}

function ChunkSummaryList({ chunks }: ChunkSummaryListProps) {
    if (chunks.length === 0) {
        return null;
    }

    return (
        <section
            className="chunk-summary-list"
            aria-labelledby="chunk-summary-list-title"
        >
            <div className="chunk-summary-list__header">
                <div>
                    <span className="chunk-summary-list__eyebrow">
                        DETAILED BREAKDOWN
                    </span>

                    <h2 id="chunk-summary-list-title">
                        Individual Chunk Summaries
                    </h2>

                    <p>
                        Explore the AI-generated summaries of individual
                        sections of your video.
                    </p>
                </div>

                <span className="chunk-summary-list__count">
                    {chunks.length} {chunks.length === 1 ? "Chunk" : "Chunks"}
                </span>
            </div>

            <div className="chunk-summary-list__items">
                {chunks.map((chunk) => (
                    <details
                        className="chunk-summary-list__item"
                        key={chunk.chunk_id}
                    >
                        <summary className="chunk-summary-list__trigger">
                            <div className="chunk-summary-list__info">
                                <strong className="chunk-summary-list__title">
                                    Chunk {chunk.chunk_id}
                                </strong>

                                <span className="chunk-summary-list__metadata">
                                    {formatDuration(chunk.start_time)}
                                    {" – "}
                                    {formatDuration(chunk.end_time)}
                                    {" · "}
                                    {chunk.word_count.toLocaleString()} words
                                </span>
                            </div>

                            <span
                                className="chunk-summary-list__chevron"
                                aria-hidden="true"
                            />
                        </summary>

                        <div className="chunk-summary-list__content">
                            <MarkdownRenderer content={chunk.summary} />
                        </div>
                    </details>
                ))}
            </div>
        </section>
    );
}

export default ChunkSummaryList;
