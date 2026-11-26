
from dataclasses import dataclass
from typing import Any, Sequence

import httpx

from app.core.config import Settings, settings

from app.shared.ai.exceptions import (
    OpenRouterConfigurationError,
    OpenRouterAuthenticationError,
    OpenRouterRateLimitError,
    OpenRouterConnectionError,
    OpenRouterTimeoutError,
    OpenRouterProviderError,
    OpenRouterResponseError,
)


# ==========================================
# RESPONSE DATA MODEL
# ==========================================

@dataclass(frozen=True, slots=True)
class OpenRouterCompletion:
    """Standardized response returned by OpenRouter."""

    content: str
    model: str
    finish_reason: str | None
    usage: dict[str, Any] | None


# ==========================================
# OPENROUTER CLIENT
# ==========================================

class OpenRouterClient:
    """
    Reusable asynchronous OpenRouter API client.

    Uses the configured free model variant only.
    Does not switch to paid models or paid fallbacks.
    """

    CHAT_COMPLETIONS_PATH = "/chat/completions"

    def __init__(
        self,
        http_client: httpx.AsyncClient,
        app_settings: Settings = settings,
    ) -> None:

        self._http_client = http_client
        self._settings = app_settings

        configured_model = self._settings.openrouter_model

        # Enforce the project's zero-cost model policy.
        if not configured_model.endswith(":free"):
            raise OpenRouterConfigurationError(
                "KhyathiAI only permits explicitly free "
                "OpenRouter model variants."
            )

        self._endpoint = (
            self._settings.openrouter_base_url.rstrip("/")
            + self.CHAT_COMPLETIONS_PATH
        )

    # ======================================
    # API KEY VALIDATION
    # ======================================

    def _get_api_key(self) -> str:
        """Returns the configured API key securely."""

        api_key = self._settings.openrouter_api_key

        if api_key is None:
            raise OpenRouterConfigurationError(
                "OPENROUTER_API_KEY is not configured. "
                "Add it to the backend .env file."
            )

        secret_value = api_key.get_secret_value().strip()

        if not secret_value:
            raise OpenRouterConfigurationError(
                "OPENROUTER_API_KEY cannot be empty."
            )

        return secret_value

    # ======================================
    # ERROR MESSAGE EXTRACTION
    # ======================================

    @staticmethod
    def _extract_error_message(
        response: httpx.Response,
    ) -> str:

        try:
            data = response.json()

            error = data.get("error", {})

            if isinstance(error, dict):
                message = error.get("message")

                if isinstance(message, str) and message.strip():
                    return message

        except ValueError:
            pass

        return "OpenRouter returned an unsuccessful response."

    # ======================================
    # HTTP ERROR HANDLING
    # ======================================

    def _handle_http_error(
        self,
        response: httpx.Response,
    ) -> None:

        status = response.status_code
        message = self._extract_error_message(response)

        if status == 401:
            raise OpenRouterAuthenticationError(
                "OpenRouter rejected the API key. "
                "Verify that the key is valid and enabled."
            )

        if status == 429:
            raise OpenRouterRateLimitError(
                "The free OpenRouter endpoint is rate-limited. "
                "Please wait and try again."
            )

        if status in {402, 403}:
            raise OpenRouterConfigurationError(
                "OpenRouter rejected access to the configured "
                "free model. No paid fallback will be attempted. "
                f"Provider message: {message}"
            )

        if status >= 500:
            raise OpenRouterProviderError(
                "The OpenRouter provider is temporarily "
                "unavailable. Please try again later."
            )

        raise OpenRouterResponseError(
            f"OpenRouter request failed with HTTP {status}: "
            f"{message}"
        )

    # ======================================
    # CHAT COMPLETION
    # ======================================

    async def generate(
        self,
        messages: Sequence[dict[str, str]],
        *,
        max_tokens: int = 2048,
        temperature: float = 0.2,
    ) -> OpenRouterCompletion:
        """
        Sends a chat completion request to OpenRouter.

        Returns the assistant's text and response metadata.
        """

        # Validate messages.
        if not messages:
            raise ValueError(
                "At least one chat message is required."
            )

        allowed_roles = {
            "system",
            "user",
            "assistant",
        }

        validated_messages = []

        for message in messages:

            role = message.get("role")
            content = message.get("content")

            if role not in allowed_roles:
                raise ValueError(
                    f"Unsupported message role: {role}"
                )

            if not isinstance(content, str) or not content.strip():
                raise ValueError(
                    "Chat message content cannot be empty."
                )

            validated_messages.append({
                "role": role,
                "content": content,
            })

        # Validate generation parameters.
        if (
            not isinstance(max_tokens, int)
            or isinstance(max_tokens, bool)
            or max_tokens <= 0
        ):
            raise ValueError(
                "max_tokens must be a positive integer."
            )

        if not isinstance(temperature, (int, float)) or isinstance(
            temperature, bool
        ):
            raise ValueError(
                "temperature must be numeric."
            )

        if not 0 <= temperature <= 2:
            raise ValueError(
                "temperature must be between 0 and 2."
            )

        # Obtain the API key.
        api_key = self._get_api_key()

        # Construct the request.
        payload = {
            "model": self._settings.openrouter_model,
            "messages": validated_messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "reasoning": {
                "enabled": True,
                "exclude": True,
            },
        }

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        # Send request.
        try:

            response = await self._http_client.post(
                self._endpoint,
                headers=headers,
                json=payload,
            )

        except httpx.TimeoutException as exc:
            raise OpenRouterTimeoutError(
                "The OpenRouter request timed out."
            ) from exc

        except httpx.RequestError as exc:
            raise OpenRouterConnectionError(
                "Unable to connect to OpenRouter."
            ) from exc

        # Handle unsuccessful HTTP responses.
        if not response.is_success:
            self._handle_http_error(response)

        # Parse JSON response.
        try:
            data = response.json()

        except ValueError as exc:
            raise OpenRouterResponseError(
                "OpenRouter returned an invalid JSON response."
            ) from exc

        # Extract completion.
        choices = data.get("choices")

        if not isinstance(choices, list) or not choices:
            raise OpenRouterResponseError(
                "OpenRouter response does not contain any choices."
            )

        first_choice = choices[0]

        if not isinstance(first_choice, dict):
            raise OpenRouterResponseError(
                "OpenRouter returned an invalid choice."
            )

        message = first_choice.get("message", {})

        if not isinstance(message, dict):
            raise OpenRouterResponseError(
                "OpenRouter returned an invalid message."
            )

        content = message.get("content")

        if not isinstance(content, str) or not content.strip():
            raise OpenRouterResponseError(
                "The AI model returned an empty response."
            )

        return OpenRouterCompletion(
            content=content.strip(),
            model=data.get("model", self._settings.openrouter_model),
            finish_reason=first_choice.get("finish_reason"),
            usage=data.get("usage"),
        )
