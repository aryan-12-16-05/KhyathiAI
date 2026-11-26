
import { useState } from "react";

import "./CopyButton.css";

interface CopyButtonProps {
    text: string;
    label?: string;
    successLabel?: string;
}

function CopyButton({
    text,
    label = "Copy",
    successLabel = "Copied!",
}: CopyButtonProps) {
    const [status, setStatus] = useState<
        "idle" | "success" | "error"
    >("idle");

    const handleCopy = async () => {
        if (!text.trim()) {
            setStatus("error");
            return;
        }

        try {
            if (!navigator.clipboard?.writeText) {
                throw new Error("Clipboard access is unavailable.");
            }

            await navigator.clipboard.writeText(text);

            setStatus("success");
        } catch {
            setStatus("error");
        }
    };

    return (
        <div className="copy-button-container">
            <button
                type="button"
                className="copy-button"
                onClick={handleCopy}
                disabled={!text.trim()}
                aria-label={
                    status === "success"
                        ? successLabel
                        : status === "error"
                            ? "Copy failed"
                            : label
                }
            >
                {status === "success" ? successLabel : label}
            </button>

            <span
                className="copy-button__feedback"
                role="status"
                aria-live="polite"
            >
                {status === "error" && "Unable to copy. Check browser permissions."}
            </span>
        </div>
    );
}

export default CopyButton;
