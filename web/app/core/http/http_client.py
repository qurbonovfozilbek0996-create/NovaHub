from __future__ import annotations

from typing import Any

import httpx


class HttpClient:
    def __init__(
        self,
        base_url: str,
        timeout: int = 30,
    ) -> None:
        self._client = httpx.AsyncClient(
            base_url=base_url,
            timeout=timeout,
        )

    async def get(
        self,
        url: str,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:

        response = await self._client.get(
            url,
            params=params,
        )

        response.raise_for_status()

        return response.json()

    async def post(
        self,
        url: str,
        data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:

        response = await self._client.post(
            url,
            data=data,
        )

        response.raise_for_status()

        return response.json()

    async def close(self) -> None:
        await self._client.aclose()
