from sqlalchemy.ext.asyncio import AsyncSession
from modules.users.domain.unit_of_work import IUnitOfWork
from modules.users.infrastructure.sqlalchemy_repository import SQLAlchemyUserRepository


class SQLAlchemyUnitOfWork(IUnitOfWork):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def __aenter__(self):
        self.users = SQLAlchemyUserRepository(self.session)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if exc_type:
            await self.rollback()
        # else:
            # await self.commit()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()