from app.services.permission_service import PermissionService
from app.services.role_permission_service import RolePermissionService
from app.services.role_service import RoleService


class RolePermissionSeeder:
    """
    NovaHub Role Permission Seeder.
    """

    def __init__(
        self,
        role_service: RoleService,
        permission_service: PermissionService,
        role_permission_service: RolePermissionService,
    ):
        self.role_service = role_service
        self.permission_service = permission_service
        self.role_permission_service = role_permission_service

    async def run(self) -> None:
        """
        Hozircha skelet.

        Keyingi bosqichda:
        - Founder -> barcha permissionlar
        - Admin -> admin permissionlari
        - Support -> support permissionlari
        - Moderator -> moderator permissionlari

        avtomatik biriktiriladi.
        """
        return
