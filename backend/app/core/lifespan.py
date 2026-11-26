
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import httpx

from fastapi import FastAPI


@asynccontextmanager
async def app_lifespan(
    app: FastAPI,
) -> AsyncIterator[None]:
    """
    Manages shared application resources.

    A single HTTP client is shared across API requests
    and closed automatically during application shutdown.
    """

    timeout = httpx.Timeout(
        180.0,
        connect=20.0,
    )

    async with httpx.AsyncClient(
        timeout=timeout,
    ) as http_client:

        app.state.http_client = http_client

        try:
            yield

        finally:
            del app.state.http_client
