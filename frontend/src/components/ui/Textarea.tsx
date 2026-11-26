
import { useId, type TextareaHTMLAttributes } from "react";
import "./Field.css";
import "./Textarea.css";

type TextareaSize = "small" | "medium" | "large";

interface TextareaProps
    extends TextareaHTMLAttributes<HTMLTextAreaElement> {
    label?: string;
    helperText?: string;
    error?: string;
    textareaSize?: TextareaSize;
    wrapperClassName?: string;
}

function Textarea({
    id,
    label,
    helperText,
    error,
    textareaSize = "medium",
    className = "",
    wrapperClassName = "",
    disabled = false,
    required = false,
    rows = 4,
    "aria-describedby": externalDescribedBy,
    "aria-invalid": externalAriaInvalid,
    ...textareaProps
}: TextareaProps) {
    const generatedId = useId();
    const textareaId = id ?? generatedId;

    const messageId = error
        ? `${textareaId}-error`
        : helperText
            ? `${textareaId}-helper`
            : undefined;

    const describedBy = [
        externalDescribedBy,
        messageId,
    ]
        .filter(Boolean)
        .join(" ") || undefined;

    const textareaClasses = [
        "ui-textarea",
        `ui-textarea--${textareaSize}`,
        disabled ? "is-disabled" : "",
        error ? "has-error" : "",
        className,
    ]
        .filter(Boolean)
        .join(" ");

    const wrapperClasses = [
        "ui-field",
        wrapperClassName,
    ]
        .filter(Boolean)
        .join(" ");

    return (
        <div className={wrapperClasses}>
            {label && (
                <label
                    htmlFor={textareaId}
                    className="ui-field__label"
                >
                    {label}

                    {required && (
                        <span className="ui-field__required" aria-hidden="true">
                            {" "}*
                        </span>
                    )}
                </label>
            )}

            <textarea
                id={textareaId}
                className={textareaClasses}
                rows={rows}
                disabled={disabled}
                required={required}
                aria-invalid={error ? true : externalAriaInvalid}
                aria-describedby={describedBy}
                {...textareaProps}
            />

            {error ? (
                <p
                    id={`${textareaId}-error`}
                    className="ui-field__error"
                    role="alert"
                >
                    {error}
                </p>
            ) : helperText ? (
                <p
                    id={`${textareaId}-helper`}
                    className="ui-field__helper"
                >
                    {helperText}
                </p>
            ) : null}
        </div>
    );
}

export default Textarea;
