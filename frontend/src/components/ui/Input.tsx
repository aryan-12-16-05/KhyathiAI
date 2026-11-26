
import "./Field.css";
import { useId, type InputHTMLAttributes } from "react";

import "./Input.css";

type InputSize = "small" | "medium" | "large";

interface InputProps extends Omit<InputHTMLAttributes<HTMLInputElement>, "size"> {
    label?: string;
    helperText?: string;
    error?: string;
    inputSize?: InputSize;
    wrapperClassName?: string;
}

function Input({
    id,
    label,
    helperText,
    error,
    inputSize = "medium",
    className = "",
    wrapperClassName = "",
    disabled = false,
    required = false,
    "aria-describedby": externalDescribedBy,
    "aria-invalid": externalAriaInvalid,
    ...inputProps
}: InputProps) {
    const generatedId = useId();
    const inputId = id ?? generatedId;

    const messageId = error
        ? `${inputId}-error`
        : helperText
            ? `${inputId}-helper`
            : undefined;

    const describedBy = [
        externalDescribedBy,
        messageId,
    ]
        .filter(Boolean)
        .join(" ") || undefined;

    const inputClasses = [
        "ui-input",
        `ui-input--${inputSize}`,
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
                    htmlFor={inputId}
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

            <input
                id={inputId}
                className={inputClasses}
                disabled={disabled}
                required={required}
                aria-invalid={error ? true : externalAriaInvalid}
                aria-describedby={describedBy}
                {...inputProps}
            />

            {error ? (
                <p
                    id={`${inputId}-error`}
                    className="ui-field__error"
                    role="alert"
                >
                    {error}
                </p>
            ) : helperText ? (
                <p
                    id={`${inputId}-helper`}
                    className="ui-field__helper"
                >
                    {helperText}
                </p>
            ) : null}
        </div>
    );
}

export default Input;
