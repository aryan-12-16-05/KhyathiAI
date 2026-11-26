
import { useSummarizer } from "../features/summarizer/hooks/useSummarizer";

import SummarizerForm from "../features/summarizer/components/SummarizerForm";

import SummarizationResults from "../features/summarizer/components/SummarizationResults";

import "./SummarizerPage.css";

function SummarizerPage() {
    const {
        result,
        isLoading,
        error,
        summarize,
    } = useSummarizer();

    return (
        <main className="summarizer-page">
            <section className="summarizer-page__hero">

                <span className="summarizer-page__eyebrow">
                    KhyathiAI INTELLIGENCE
                </span>

                <h1 className="summarizer-page__title">
                    Understand more.
                    <br />
                    Watch less.
                </h1>

                <p className="summarizer-page__description">
                    Transform lengthy YouTube videos into clear,
                    structured summaries with AI. Save time and focus
                    on what matters.
                </p>

                <div className="summarizer-page__form-container">
                    <SummarizerForm
                        isLoading={isLoading}
                        onSubmit={summarize}
                    />
                </div>

                {/* Loading state */}

                {isLoading && (
                    <div
                        className="summarizer-page__status"
                        role="status"
                        aria-live="polite"
                    >
                        <span
                            className="summarizer-page__status-indicator"
                            aria-hidden="true"
                        />

                        <div>
                            <strong>Analyzing your video...</strong>

                            <p>
                                Retrieving the transcript and generating your
                                summary. This may take a little while.
                            </p>
                        </div>
                    </div>
                )}

                {/* Error state */}

                {error && (
                    <div
                        className="summarizer-page__error"
                        role="alert"
                    >
                        <strong>Unable to generate summary</strong>
                        <p>{error}</p>
                    </div>
                )}

            </section>

            {/* Actual AI-generated results */}

            {result && (
                <div className="summarizer-page__results">
                    <SummarizationResults data={result} />
                </div>
            )}

        </main>
    );
}

export default SummarizerPage;
