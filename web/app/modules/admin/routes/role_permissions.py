from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies.services import get_db_session
from app.modules.admin.services.role_permission_service import (
    RolePermissionService,
)


router = APIRouter(
    prefix="/admin/roles",
    tags=["Admin Role Permissions"],
)


@router.get("/{role_id}/permissions")
async def list_role_permissions(
    role_id: int,
    session: AsyncSession = Depends(get_db_session),
):
    service = RolePermissionService(session)

    permissions = await service.get_role_permissions(role_id)

    return {
        "success": True,
        "role_id": role_id,
        "permissions": [
            {
                "id": permission.id,
                "module": permission.module,
                "action": permission.action,
                "code": permission.code,
            }
            for permission in permissions
        ],
    }

@router.post("/{role_id}/permissions/{permission_id}")
async def add_role_permission(
    role_id: int,
    permission_id: int,
    session: AsyncSession = Depends(get_db_session),
):
    service = RolePermissionService(session)

    result = await service.add_permission(
        role_id,
        permission_id,
    )

    return {
        "success": True,
        "message": "Permission added",
        "role_permission_id": result.id,
    }


@router.delete("/{role_id}/permissions/{permission_id}")
async def remove_role_permission(
    role_id: int,
    permission_id: int,
    session: AsyncSession = Depends(get_db_session),
):
    service = RolePermissionService(session)

    result = await service.remove_permission(
        role_id,
        permission_id,
    )

    return {
        "success": result,
        "message": (
            "Permission removed"
            if result
            else "Permission not found"
        ),
    }

@router.delete("/{role_id}/permissions/{permission_id}")
async def remove_role_permission(
    role_id: int,
    permission_id: int,
    session: AsyncSession = Depends(get_db_session),
):
    service = RolePermissionService(session)

    success = await service.remove_permission(
        role_id,
        permission_id,
    )

    if not success:
        return {
            "success": False,
            "message": "Permission not found",
        }

    return {
        "success": True,
        "message": "Permission removed",
    }
