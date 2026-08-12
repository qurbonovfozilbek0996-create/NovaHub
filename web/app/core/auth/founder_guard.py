from app.core.auth.auth_context import AuthContext


class FounderGuard:
    """
    NovaHub Founder Guard.

    Founder yoki Founder tomonidan berilgan
    maxsus ruxsatlarni tekshiradi.
    """

    def __init__(self, auth: AuthContext):
        self.auth = auth

    async def require_founder(self) -> bool:
        """
        Faqat Founder kirishi mumkin.
        """
        return self.auth.is_founder

    async def require_permission(
        self,
        permission_code: str,
    ) -> bool:
        """
        Hozircha skelet.

        Keyinchalik Founder yoki
        maxsus permissionga ega administratorni
        tekshiradi.
        """
        if self.auth.is_founder:
            return True

        return False
