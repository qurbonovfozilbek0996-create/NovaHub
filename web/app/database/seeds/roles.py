from app.database.seeds.constants import SYSTEM_ROLES
from app.models.role import Role
from app.services.role_service import RoleService


class RoleSeeder:
    """
    NovaHub Role Seeder.
    """

    def __init__(self, role_service: RoleService):
        self.role_service = role_service

    async def run(self) -> None:
        """
        System rollarni yaratadi.
        """

        for item in SYSTEM_ROLES:

            role = await self.role_service.get_by_code(
                item["code"]
            )

            if role is not None:
                continue

            await self.role_service.create(
                Role(
                    name=item["name"],
                    code=item["code"],
                    description=item.get("description"),
                    is_system=True,
                    is_active=True,
                )
            )
