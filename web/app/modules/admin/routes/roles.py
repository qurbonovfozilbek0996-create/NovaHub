from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies.services import get_db_session
from app.modules.admin.services.roles_service import RolesService


router = APIRouter(
    prefix="/admin/roles",
    tags=["Admin Roles"],
)


@router.get("/")
async def list_roles(
    session: AsyncSession = Depends(get_db_session),
):
    service = RolesService(session)

    roles = await service.get_roles()

    return {
        "success": True,
        "count": len(roles),
        "roles": [
            {
                "id": role.id,
                "name": role.name,
                "code": role.code,
                "description": role.description,
            }
            for role in roles
        ],
    }


@router.get("/{role_id}")
async def get_role(
    role_id: int,
    session: AsyncSession = Depends(get_db_session),
):
    service = RolesService(session)

    role = await service.get_role(role_id)

    if not role:
        return {
            "success": False,
            "message": "Role not found",
        }

    permissions = await service.get_role_permissions(role_id)

    return {
        "success": True,
        "role": {
            "id": role.id,
            "name": role.name,
            "code": role.code,
            "description": role.description,
            "permissions": [
                {
                    "id": permission.id,
                    "module": permission.module,
                    "action": permission.action,
                    "code": permission.code,
                }
                for permission in permissions
            ],
        },
    }
