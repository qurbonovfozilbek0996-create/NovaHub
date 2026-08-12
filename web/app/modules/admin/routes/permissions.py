from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies.services import get_db_session
from app.models.permission import Permission
from sqlalchemy import select


router = APIRouter(
    prefix="/admin/permissions",
    tags=["Admin Permissions"],
)


@router.get("/")
async def list_permissions(
    session: AsyncSession = Depends(get_db_session),
):
    result = await session.execute(
        select(Permission)
        .order_by(Permission.id)
    )

    permissions = result.scalars().all()

    return {
        "success": True,
        "count": len(permissions),
        "permissions": [
            {
                "id": permission.id,
                "module": permission.module,
                "action": permission.action,
                "code": permission.code,
                "description": permission.description,
            }
            for permission in permissions
        ],
    }
