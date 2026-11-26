
import asyncio

import httpx

from app.core.config import settings

from app.shared.ai.openrouter_client import OpenRouterClient

from app.shared.ai.exceptions import OpenRouterError


async def verify_openrouter_connection() -> None:
    """
    Sends a small real request to the configured
    free OpenRouter model and verifies its response.
    """

    timeout = httpx.Timeout(
        180.0,
        connect=20.0,
    )

    async with httpx.AsyncClient(
        timeout=timeout
    ) as http_client:

        client = OpenRouterClient(
            http_client=http_client,
            app_settings=settings,
        )

        completion = await client.generate(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Answer in simple English "
                        "using one or two sentences."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        "What is machine learning?"
                    ),
                },
            ],
            max_tokens=2048,
            temperature=0.2,
        )

    print("\nLIVE OPENROUTER REQUEST SUCCESSFUL!")

    print("Configured model:", settings.openrouter_model)
    print("Served model:", completion.model)
    print("Finish reason:", completion.finish_reason)

    print("\nAI RESPONSE:")
    print(completion.content)

    if completion.usage:
        print("\nTOKEN USAGE:")
        print(completion.usage)


async def main() -> None:

    try:
        await verify_openrouter_connection()

    except OpenRouterError as exc:

        print("\nOPENROUTER REQUEST FAILED!")
        print("Error type:", type(exc).__name__)
        print("Error:", exc)

        raise SystemExit(1)


if __name__ == "__main__":
    asyncio.run(main())
