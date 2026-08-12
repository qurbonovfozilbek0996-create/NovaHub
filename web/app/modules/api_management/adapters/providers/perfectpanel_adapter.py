from typing import Any

from app.core.http.http_client import HttpClient
from app.modules.api_management.adapters.base.base_adapter import (
    BaseProviderAdapter,
)
from app.modules.api_management.models.provider import Provider


class PerfectPanelAdapter(BaseProviderAdapter):
    def __init__(
        self,
        provider: Provider,
    ) -> None:
        self.provider = provider

        api_version = str(
            provider.api_version or "v2"
        ).strip().strip("/")

        if not api_version.startswith("v"):
            api_version = f"v{api_version}"

        self.api_version = api_version

        self.client = HttpClient(
            base_url=provider.base_url.rstrip("/"),
            timeout=provider.timeout,
        )

    async def _request(
        self,
        action: str,
        **params: Any,
    ) -> dict[str, Any] | list[Any]:

        payload = {
            "key": self.provider.api_key,
            "action": action,
            **params,
        }

        return await self.client.post(
            f"/api/{self.api_version}",
            data=payload,
        )

    async def test_connection(
        self,
    ) -> bool:
        try:
            await self.get_balance()
            return True
        except Exception:
            return False

    async def get_balance(
        self,
    ) -> float:

        response = await self._request(
            "balance"
        )

        if not isinstance(response, dict):
            raise ValueError(
                "Invalid balance response."
            )

        balance = response.get("balance")

        if balance is None:
            raise ValueError(
                "Balance not found in API response."
            )

        try:
            return float(balance)
        except (TypeError, ValueError) as exc:
            raise ValueError(
                "Invalid balance value."
            ) from exc

    async def sync_services(
        self,
    ) -> list[dict[str, Any]]:

        response = await self._request(
            "services"
        )

        if not isinstance(response, list):
            raise ValueError(
                "Invalid services response."
            )

        return [
            service
            for service in response
            if isinstance(service, dict)
        ]

    async def get_service(
        self,
        service_id: int,
    ) -> dict[str, Any]:

        services = await self.sync_services()

        target_id = str(service_id)

        for service in services:
            remote_id = service.get("service")

            if remote_id is not None and str(
                remote_id
            ) == target_id:
                return service

        raise ValueError(
            "Service not found."
        )

    async def create_order(
        self,
        **kwargs: Any,
    ) -> dict[str, Any]:

        response = await self._request(
            "add",
            **kwargs,
        )

        if not isinstance(response, dict):
            raise ValueError(
                "Invalid order response."
            )

        return response

    async def get_order_status(
        self,
        order_id: int,
    ) -> dict[str, Any]:

        response = await self._request(
            "status",
            order=order_id,
        )

        if not isinstance(response, dict):
            raise ValueError(
                "Invalid order status response."
            )

        return response

    async def cancel_order(
        self,
        order_id: int,
    ) -> dict[str, Any]:

        response = await self._request(
            "cancel",
            order=order_id,
        )

        if not isinstance(response, dict):
            raise ValueError(
                "Invalid cancel response."
            )

        return response
