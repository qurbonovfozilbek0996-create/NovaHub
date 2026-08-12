from app.database.seeds.constants import SYSTEM_PERMISSIONS
from app.models.permission import Permission
from app.services.permission_service import PermissionService


class PermissionSeeder:
    """
    NovaHub Permission Seeder.
    """

    def __init__(
        self,
        permission_service: PermissionService,
    ):
        self.permission_service = permission_service

    async def run(self) -> None:
        """
        System permissionlarini yaratadi.
        """

        for item in SYSTEM_PERMISSIONS:

            permission = (
                await self.permission_service.get_by_code(
                    item["code"]
                )
            )

            if permission is not None:
                continue

            await self.permission_service.create(
                Permission(
                    module=item["module"],
                    action=item["action"],
                    code=item["code"],
                    description=item.get("description"),
                    is_system=True,
                    is_active=True,
                )
            )
