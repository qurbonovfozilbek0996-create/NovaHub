from sqlalchemy.ext.asyncio import AsyncSession


class UnitOfWork:
    """
    NovaHub Unit of Work.

    Bir nechta service ichma-ich UnitOfWork ishlatganda
    transaction faqat eng tashqi UnitOfWork tomonidan
    commit qilinadi.

    Shu orqali:
        Wallet update
        + Transaction
        + Payment update

    kabi operatsiyalar bitta database transaction
    sifatida bajarilishi mumkin.
    """

    _DEPTH_KEY = "novahub_uow_depth"
    _ROLLBACK_KEY = "novahub_uow_rollback"

    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session

    async def __aenter__(self):
        depth = self.session.info.get(
            self._DEPTH_KEY,
            0,
        )

        self.session.info[self._DEPTH_KEY] = depth + 1

        if depth == 0:
            self.session.info[self._ROLLBACK_KEY] = False

        return self

    async def __aexit__(
        self,
        exc_type,
        exc,
        tb,
    ):
        depth = self.session.info.get(
            self._DEPTH_KEY,
            1,
        )

        if exc is not None:
            self.session.info[self._ROLLBACK_KEY] = True

        depth -= 1

        self.session.info[self._DEPTH_KEY] = max(
            depth,
            0,
        )

        if depth > 0:
            return False

        rollback_required = self.session.info.pop(
            self._ROLLBACK_KEY,
            False,
        )

        self.session.info.pop(
            self._DEPTH_KEY,
            None,
        )

        if rollback_required:
            await self.rollback()
        else:
            await self.commit()

        return False

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
