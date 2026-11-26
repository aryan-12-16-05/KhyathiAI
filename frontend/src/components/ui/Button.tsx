
import type { ButtonHTMLAttributes } from "react";

import "./Button.css";

type ButtonVariant = "primary" | "secondary" | "outline" | "ghost";

type ButtonSize = "small" | "medium" | "large";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
    variant?: ButtonVariant;
    size?: ButtonSize;
    loading?: boolean;
}

function Button({
    children,
    variant = "primary",
    size = "medium",
    loading = false,
    disabled = false,
    type = "button",
    className = "",
    ...props
}: ButtonProps) {
    const buttonClasses = [
        "ui-button",
        `ui-button--${variant}`,
        `ui-button--${size}`,
        className,
    ]
        .filter(Boolean)
        .join(" ");

    return (
        <button
            type={type}
            className={buttonClasses}
            disabled={disabled || loading}
            aria-busy={loading || undefined}
            {...props}
        >
            {loading && (
                <span className="ui-button__spinner" aria-hidden="true" />
            )}

            {children}
        </button>
    );
}

export default Button;
