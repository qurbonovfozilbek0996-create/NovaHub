from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.audit_log import AuditLog
from app.repositories.base_repository import BaseRepository


class AuditRepository(BaseRepository):
    """
    Audit log repository.
    """

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_by_id(self, audit_id: int) -> AuditLog | None:
        result = await self.session.execute(
            select(AuditLog).where(AuditLog.id == audit_id)
        )
        return result.scalar_one_or_none()

    async def get_user_logs(
        self,
        user_id: int,
    ) -> list[AuditLog]:
        result = await self.session.execute(
            select(AuditLog)
            .where(AuditLog.user_id == user_id)
            .order_by(AuditLog.created_at.desc())
        )
        return list(result.scalars().all())

    async def create(
        self,
        audit_log: AuditLog,
    ) -> AuditLog:
        self.session.add(audit_log)
        await self.session.flush()
        await self.session.refresh(audit_log)
        return audit_log
