"""
NovaHub Database Seeder
"""

from sqlalchemy import select

from app.models.role import Role
from app.models.permission import Permission
from app.models.role_permission import RolePermission
from app.models.user import User

from app.database.seeds.constants import (
    SYSTEM_ROLES,
    SYSTEM_PERMISSIONS,
)


class DatabaseSeeder:
    """
    NovaHub database seeder.
    """

    def __init__(self, session):
        self.session = session


    async def run(self) -> None:
        await self.seed_roles()
        await self.seed_permissions()
        await self.seed_role_permissions()


    async def seed_roles(self) -> None:
        for data in SYSTEM_ROLES:

            result = await self.session.execute(
                select(Role).where(
                    Role.code == data["code"]
                )
            )

            role = result.scalar_one_or_none()

            if not role:
                role = Role(
                    name=data["name"],
                    code=data["code"],
                    description=data["description"],
                    is_system=True,
                )

                self.session.add(role)

        await self.session.flush()

    async def seed_permissions(self) -> None:
        for data in SYSTEM_PERMISSIONS:

            result = await self.session.execute(
                select(Permission).where(
                    Permission.code == data["code"]
                )
            )

            permission = result.scalar_one_or_none()

            if not permission:
                permission = Permission(
                    module=data["module"],
                    action=data["action"],
                    code=data["code"],
                    description=data["description"],
                    is_system=True,
                )

                self.session.add(permission)

        await self.session.flush()

    async def seed_role_permissions(self) -> None:
        result = await self.session.execute(
            select(Role).where(
                Role.code == "founder"
            )
        )

        founder_role = result.scalar_one_or_none()

        if not founder_role:
            return

        permissions = await self.session.execute(
            select(Permission)
        )

        permissions = permissions.scalars().all()

        for permission in permissions:

            existing = await self.session.execute(
                select(RolePermission).where(
                    RolePermission.role_id == founder_role.id,
                    RolePermission.permission_id == permission.id,
                )
            )

            role_permission = existing.scalar_one_or_none()

            if not role_permission:
                self.session.add(
                    RolePermission(
                        role_id=founder_role.id,
                        permission_id=permission.id,
                        is_active=True,
                    )
                )

        await self.session.flush()

    async def seed_founder(self) -> None:
        founder_telegram_id = 8211219159

        result = await self.session.execute(
            select(User).where(
                User.telegram_id == founder_telegram_id
            )
        )

        founder = result.scalar_one_or_none()

        if founder:
            return

        role_result = await self.session.execute(
            select(Role).where(
                Role.code == "founder"
            )
        )

        founder_role = role_result.scalar_one_or_none()

        if not founder_role:
            return

        founder = User(
            telegram_id=founder_telegram_id,
            full_name="Founder",
            username="founder",
            language="uz",
            role_id=founder_role.id,
            is_active=True,
            is_banned=False,
        )

        self.session.add(founder)

        await self.session.flush()
