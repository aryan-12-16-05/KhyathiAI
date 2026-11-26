
import type { SummarizationResponse } from "../types";

import { formatDuration } from "../utils/formatDuration";

import "./VideoMetadata.css";

interface VideoMetadataProps {
    data: SummarizationResponse;
}

function VideoMetadata({ data }: VideoMetadataProps) {
    const captionType = data.is_generated
        ? "Auto-generated"
        : "Manually created";

    const translationStatus = data.was_translated
        ? "Translated into English"
        : "Original captions";

    const metadataItems = [
        {
            label: "Duration",
            value: formatDuration(data.duration_seconds),
        },
        {
            label: "Language",
            value: data.language,
        },
        {
            label: "Transcript words",
            value: data.transcript_word_count.toLocaleString(),
        },
        {
            label: "Chunks processed",
            value: data.chunk_count.toString(),
        },
        {
            label: "Caption type",
            value: captionType,
        },
        {
            label: "Translation",
            value: translationStatus,
        },
    ];

    return (
        <section
            className="video-metadata"
            aria-labelledby="video-metadata-title"
        >
            <div className="video-metadata__header">
                <h2 id="video-metadata-title">
                    Video Information
                </h2>

                <span className="video-metadata__status">
                    Processing completed
                </span>
            </div>

            <div className="video-metadata__grid">
                {metadataItems.map((item) => (
                    <div
                        className="video-metadata__item"
                        key={item.label}
                    >
                        <span className="video-metadata__label">
                            {item.label}
                        </span>

                        <strong className="video-metadata__value">
                            {item.value}
                        </strong>
                    </div>
                ))}
            </div>
        </section>
    );
}

export default VideoMetadata;
