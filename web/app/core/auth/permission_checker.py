from app.core.auth.auth_context import AuthContext


class PermissionChecker:
    """
    NovaHub Permission Checker.

    Barcha permission tekshiruvlari shu klass
    orqali amalga oshiriladi.
    """

    def __init__(self, auth: AuthContext):
        self.auth = auth

    def is_founder(self) -> bool:
        return self.auth.is_founder

    def has_role(self, role_code: str) -> bool:
        if self.auth.role is None:
            return False

        return self.auth.role.code == role_code

    async def has_permission(
        self,
        permission_code: str,
    ) -> bool:
        """
        Hozircha skelet.

        Keyinchalik RolePermission va
        UserPermission orqali tekshiradi.
        """
        return False
