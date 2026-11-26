
import type { HTMLAttributes } from "react";

import "./Card.css";

type CardVariant = "default" | "outlined" | "elevated";

type CardPadding = "none" | "small" | "medium" | "large";

interface CardProps extends HTMLAttributes<HTMLDivElement> {
    variant?: CardVariant;
    padding?: CardPadding;
}

function Card({
    children,
    variant = "default",
    padding = "medium",
    className = "",
    ...props
}: CardProps) {
    const cardClasses = [
        "ui-card",
        `ui-card--${variant}`,
        `ui-card--padding-${padding}`,
        className,
    ]
        .filter(Boolean)
        .join(" ");

    return (
        <div className={cardClasses} {...props}>
            {children}
        </div>
    );
}

export default Card;
