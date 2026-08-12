from app.modules.api_management.adapters.providers.perfectpanel_adapter import (
    PerfectPanelAdapter,
)
from app.modules.api_management.models.provider import (
    Provider,
    ProviderType,
)


class ProviderFactory:
    @staticmethod
    def create(provider: Provider):
        if provider.provider_type == ProviderType.SMM:
            return PerfectPanelAdapter(provider)

        raise ValueError(
            f"Unsupported provider type: {provider.provider_type.value}"
        )
