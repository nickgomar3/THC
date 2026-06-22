from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from modules.users.domain import User, IUserRepository


class SQLAlchemyUserRepository(IUserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self):
        result = await self.session.execute(select(User))
        return result.scalars().all()
    
    async def get_by_id(self, user_id: int):
        return await self.session.get(User, user_id)

    async def add(self, user: User):
        self.session.add(user)
        
    async def update(self, user: User):
        await self.session.merge(user)

    async def delete(self, user: User):
        await self.session.delete(user)