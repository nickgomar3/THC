from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from modules.users.domain import User, IUserRepository


class SQLAlchemyUserRepository(IUserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session


    async def get(self):
        query = select(User).options(selectinload(User.pokemons))
        result = await self.session.execute(query)
        return result.scalars().all()

    
    async def get_by_id(self, user_id: int):
        query = (
            select(User)
            .options(selectinload(User.pokemons))
            .filter(User.id == user_id)
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()


    async def add(self, user: User):
        self.session.add(user)
        
    async def update(self, user: User):
        await self.session.merge(user)

    async def delete(self, user: User):
        await self.session.delete(user)