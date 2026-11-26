
import json
import unittest

import httpx

from pydantic import SecretStr

from app.core.config import Settings

from app.shared.ai.openrouter_client import OpenRouterClient

from app.shared.ai.exceptions import (
    OpenRouterConfigurationError,
    OpenRouterAuthenticationError,
    OpenRouterRateLimitError,
    OpenRouterProviderError,
    OpenRouterResponseError,
    OpenRouterTimeoutError,
)


TEST_MODEL = "nvidia/nemotron-3-ultra-550b-a55b:free"


def create_settings(
    api_key: str | None = "test-api-key",
    model: str = TEST_MODEL,
) -> Settings:

    return Settings(
        openrouter_api_key=(
            SecretStr(api_key) if api_key is not None else None
        ),
        openrouter_model=model,
    )


class TestOpenRouterClient(unittest.IsolatedAsyncioTestCase):

    async def test_successful_completion(self):

        def handler(request):

            self.assertEqual(
                request.url.path,
                "/api/v1/chat/completions",
            )

            self.assertEqual(
                request.headers["Authorization"],
                "Bearer test-api-key",
            )

            payload = json.loads(request.content)

            self.assertEqual(payload["model"], TEST_MODEL)
            self.assertEqual(payload["max_tokens"], 2048)
            self.assertEqual(payload["temperature"], 0.2)

            self.assertTrue(payload["reasoning"]["enabled"])
            self.assertTrue(payload["reasoning"]["exclude"])

            return httpx.Response(
                200,
                json={
                    "model": TEST_MODEL,
                    "choices": [
                        {
                            "message": {
                                "role": "assistant",
                                "content": "A successful AI response.",
                            },
                            "finish_reason": "stop",
                        }
                    ],
                    "usage": {
                        "prompt_tokens": 20,
                        "completion_tokens": 15,
                        "total_tokens": 35,
                        "cost": 0,
                    },
                },
            )

        async with httpx.AsyncClient(
            transport=httpx.MockTransport(handler)
        ) as http_client:

            service = OpenRouterClient(
                http_client,
                create_settings(),
            )

            result = await service.generate([
                {
                    "role": "user",
                    "content": "Summarize this text.",
                }
            ])

        self.assertEqual(
            result.content,
            "A successful AI response.",
        )

        self.assertEqual(result.model, TEST_MODEL)
        self.assertEqual(result.finish_reason, "stop")
        self.assertEqual(result.usage["cost"], 0)

    async def test_missing_api_key(self):

        async with httpx.AsyncClient(
            transport=httpx.MockTransport(
                lambda request: httpx.Response(200)
            )
        ) as http_client:

            service = OpenRouterClient(
                http_client,
                create_settings(api_key=None),
            )

            with self.assertRaises(OpenRouterConfigurationError):
                await service.generate([
                    {
                        "role": "user",
                        "content": "Test",
                    }
                ])

    async def test_rejects_paid_model(self):

        with self.assertRaises(OpenRouterConfigurationError):

            OpenRouterClient(
                httpx.AsyncClient(),
                create_settings(model="some-paid-model"),
            )

    async def test_handles_authentication_error(self):

        def handler(request):
            return httpx.Response(
                401,
                json={
                    "error": {
                        "message": "Invalid API key",
                        "code": 401,
                    }
                },
            )

        async with httpx.AsyncClient(
            transport=httpx.MockTransport(handler)
        ) as http_client:

            service = OpenRouterClient(
                http_client,
                create_settings(),
            )

            with self.assertRaises(OpenRouterAuthenticationError):
                await service.generate([
                    {"role": "user", "content": "Test"}
                ])

    async def test_handles_rate_limit(self):

        def handler(request):
            return httpx.Response(
                429,
                json={
                    "error": {
                        "message": "Rate limit exceeded",
                        "code": 429,
                    }
                },
            )

        async with httpx.AsyncClient(
            transport=httpx.MockTransport(handler)
        ) as http_client:

            service = OpenRouterClient(
                http_client,
                create_settings(),
            )

            with self.assertRaises(OpenRouterRateLimitError):
                await service.generate([
                    {"role": "user", "content": "Test"}
                ])

    async def test_handles_provider_error(self):

        def handler(request):
            return httpx.Response(503)

        async with httpx.AsyncClient(
            transport=httpx.MockTransport(handler)
        ) as http_client:

            service = OpenRouterClient(
                http_client,
                create_settings(),
            )

            with self.assertRaises(OpenRouterProviderError):
                await service.generate([
                    {"role": "user", "content": "Test"}
                ])

    async def test_rejects_empty_completion(self):

        def handler(request):
            return httpx.Response(
                200,
                json={
                    "choices": [
                        {
                            "message": {
                                "role": "assistant",
                                "content": "",
                            },
                            "finish_reason": "stop",
                        }
                    ]
                },
            )

        async with httpx.AsyncClient(
            transport=httpx.MockTransport(handler)
        ) as http_client:

            service = OpenRouterClient(
                http_client,
                create_settings(),
            )

            with self.assertRaises(OpenRouterResponseError):
                await service.generate([
                    {"role": "user", "content": "Test"}
                ])

    async def test_validates_empty_messages(self):

        async with httpx.AsyncClient() as http_client:

            service = OpenRouterClient(
                http_client,
                create_settings(),
            )

            with self.assertRaises(ValueError):
                await service.generate([])

    async def test_validates_generation_parameters(self):

        async with httpx.AsyncClient() as http_client:

            service = OpenRouterClient(
                http_client,
                create_settings(),
            )

            with self.assertRaises(ValueError):
                await service.generate(
                    [{"role": "user", "content": "Test"}],
                    max_tokens=0,
                )


if __name__ == "__main__":
    unittest.main()
