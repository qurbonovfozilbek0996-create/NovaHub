from dataclasses import dataclass

from app.models.user import User
from app.models.role import Role


@dataclass(slots=True)
class AuthContext:
    """
    Authenticated user context.
    """

    user: User
    role: Role | None

    @property
    def is_authenticated(self) -> bool:
        return self.user is not None

    @property
    def is_founder(self) -> bool:
        return (
            self.role is not None
            and self.role.code == "founder"
        )
