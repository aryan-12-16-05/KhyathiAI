
import axios from "axios";

// ==========================================
// API CONFIGURATION
// ==========================================

const DEFAULT_API_BASE_URL = "http://127.0.0.1:8000/api/v1";
const DEFAULT_API_TIMEOUT = 300000;

const configuredBaseUrl = import.meta.env.VITE_API_BASE_URL?.trim();

const configuredTimeout = Number(
    import.meta.env.VITE_API_TIMEOUT_MS
);

const API_BASE_URL =
    configuredBaseUrl || DEFAULT_API_BASE_URL;

const API_TIMEOUT =
    Number.isFinite(configuredTimeout) && configuredTimeout > 0
        ? configuredTimeout
        : DEFAULT_API_TIMEOUT;


// ==========================================
// CENTRALIZED AXIOS INSTANCE
// ==========================================

export const apiClient = axios.create({
    baseURL: API_BASE_URL,
    timeout: API_TIMEOUT,

    headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
    },

    withCredentials: false,
});
