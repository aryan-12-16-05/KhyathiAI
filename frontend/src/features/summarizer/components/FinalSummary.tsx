
import MarkdownRenderer from "./MarkdownRenderer";

import CopyButton from "../../../components/ui/CopyButton";

import "./FinalSummary.css";

interface FinalSummaryProps {
    summary: string;
}

function FinalSummary({ summary }: FinalSummaryProps) {
    return (
        <section
            className="final-summary"
            aria-labelledby="final-summary-title"
        >
            <div className="final-summary__header">
                <div className="final-summary__heading">
                    <span className="final-summary__eyebrow">
                        AI GENERATED CONTENT
                    </span>

                    <h2 id="final-summary-title">
                        Your Video Summary
                    </h2>

                    <p>
                        Your complete video summary, organized into
                        clear and structured sections.
                    </p>
                </div>

                <CopyButton
                    text={summary}
                    label="Copy Summary"
                    successLabel="Copied!"
                />
            </div>

            <div className="final-summary__content">
                <MarkdownRenderer content={summary} />
            </div>
        </section>
    );
}

export default FinalSummary;
