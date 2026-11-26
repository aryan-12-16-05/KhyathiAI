
import "./Loader.css";

type LoaderSize = "small" | "medium" | "large";

interface LoaderProps {
    size?: LoaderSize;
    label?: string;
    showLabel?: boolean;
    className?: string;
}

function Loader({
    size = "medium",
    label = "Loading...",
    showLabel = true,
    className = "",
}: LoaderProps) {
    const loaderClasses = [
        "ui-loader",
        `ui-loader--${size}`,
        className,
    ]
        .filter(Boolean)
        .join(" ");

    return (
        <div
            className={loaderClasses}
            role="status"
            aria-label={label}
        >
            <span
                className="ui-loader__spinner"
                aria-hidden="true"
            />

            {showLabel && (
                <span className="ui-loader__label">
                    {label}
                </span>
            )}
        </div>
    );
}

export default Loader;
