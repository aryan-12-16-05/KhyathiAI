
class OpenRouterError(Exception):
    """Base exception for OpenRouter integration."""


class OpenRouterConfigurationError(OpenRouterError):
    """Raised when OpenRouter configuration is invalid."""


class OpenRouterAuthenticationError(OpenRouterError):
    """Raised when OpenRouter rejects the API key."""


class OpenRouterRateLimitError(OpenRouterError):
    """Raised when the free endpoint is rate-limited."""


class OpenRouterConnectionError(OpenRouterError):
    """Raised when OpenRouter cannot be reached."""


class OpenRouterTimeoutError(OpenRouterError):
    """Raised when an OpenRouter request times out."""


class OpenRouterProviderError(OpenRouterError):
    """Raised when the upstream AI provider fails."""


class OpenRouterResponseError(OpenRouterError):
    """Raised when the AI response is invalid or empty."""
