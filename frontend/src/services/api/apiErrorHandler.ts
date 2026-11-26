
import axios from "axios";

// ==========================================
// STANDARDIZED API ERROR
// ==========================================

export class ApiRequestError extends Error {
    readonly status?: number;
    readonly code?: string;

    constructor(
        message: string,
        status?: number,
        code?: string,
    ) {
        super(message);

        this.name = "ApiRequestError";
        this.status = status;
        this.code = code;

        Object.setPrototypeOf(this, ApiRequestError.prototype);
    }
}


// ==========================================
// BACKEND ERROR MESSAGE EXTRACTION
// ==========================================

function extractServerMessage(data: unknown): string | undefined {
    if (!data || typeof data !== "object") {
        return undefined;
    }

    const payload = data as Record<string, unknown>;

    if (typeof payload.detail === "string") {
        return payload.detail;
    }

    if (Array.isArray(payload.detail)) {
        const messages = payload.detail
            .map((item) => {
                if (
                    item &&
                    typeof item === "object" &&
                    "msg" in item &&
                    typeof item.msg === "string"
                ) {
                    return item.msg;
                }

                return undefined;
            })
            .filter((message): message is string => Boolean(message));

        if (messages.length > 0) {
            return messages.join(". ");
        }
    }

    if (typeof payload.message === "string") {
        return payload.message;
    }

    return undefined;
}


// ==========================================
// ERROR NORMALIZATION
// ==========================================

export function normalizeApiError(
    error: unknown,
): ApiRequestError {

    if (axios.isAxiosError(error)) {
        const status = error.response?.status;

        const serverMessage = extractServerMessage(
            error.response?.data,
        );

        if (serverMessage) {
            return new ApiRequestError(
                serverMessage,
                status,
                error.code,
            );
        }

        if (
            error.code === "ECONNABORTED" ||
            error.code === "ETIMEDOUT"
        ) {
            return new ApiRequestError(
                "The request timed out. Please try again.",
                status,
                error.code,
            );
        }

        if (!error.response) {
            return new ApiRequestError(
                "Unable to connect to KhyathiAI. Please check whether the backend server is running.",
                undefined,
                error.code,
            );
        }

        return new ApiRequestError(
            `The request failed with status ${status}. Please try again.`,
            status,
            error.code,
        );
    }

    if (error instanceof Error) {
        return new ApiRequestError(error.message);
    }

    return new ApiRequestError(
        "An unexpected error occurred. Please try again.",
    );
}
