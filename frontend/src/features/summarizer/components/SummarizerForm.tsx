
import { useState, type FormEvent } from "react";

import { validateYouTubeUrl } from "../utils/youtubeUrlValidator";

import "./SummarizerForm.css";

interface SummarizerFormProps {
    isLoading: boolean;
    onSubmit: (youtubeUrl: string) => Promise<void>;
}

function SummarizerForm({
    isLoading,
    onSubmit,
}: SummarizerFormProps) {
    const [youtubeUrl, setYoutubeUrl] = useState("");
    const [validationError, setValidationError] = useState<string | null>(null);

    const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
        event.preventDefault();

        const normalizedUrl = youtubeUrl.trim();

        const validationMessage = validateYouTubeUrl(normalizedUrl);

        if (validationMessage) {
            setValidationError(validationMessage);
            return;
        }

        setValidationError(null);

        void onSubmit(normalizedUrl);
    };

    const handleInputChange = (value: string) => {
        setYoutubeUrl(value);

        if (validationError) {
            setValidationError(null);
        }
    };

    return (
        <form
            className="summarizer-form"
            onSubmit={handleSubmit}
        >
            <div className="summarizer-form__field">
                <label
                    htmlFor="youtube-url"
                    className="summarizer-form__label"
                >
                    YouTube video URL
                </label>

                <input
                    id="youtube-url"
                    type="url"
                    className="summarizer-form__input"
                    placeholder="Paste your YouTube video link here..."
                    value={youtubeUrl}
                    onChange={(event) => handleInputChange(event.target.value)}
                    disabled={isLoading}
                    aria-invalid={Boolean(validationError)}
                    aria-describedby={
                        validationError ? "youtube-url-error" : "youtube-url-help"
                    }
                />

                {validationError ? (
                    <p
                        id="youtube-url-error"
                        className="summarizer-form__validation-error"
                        role="alert"
                    >
                        {validationError}
                    </p>
                ) : (
                    <p
                        id="youtube-url-help"
                        className="summarizer-form__help"
                    >
                        Supported: YouTube videos, Shorts, live and embedded URLs.
                    </p>
                )}
            </div>

            <button
                type="submit"
                className="summarizer-form__submit"
                disabled={isLoading || !youtubeUrl.trim()}
            >
                {isLoading ? (
                    <>
                        <span
                            className="summarizer-form__spinner"
                            aria-hidden="true"
                        />
                        Generating summary...
                    </>
                ) : (
                    "Generate Summary"
                )}
            </button>
        </form>
    );
}

export default SummarizerForm;
