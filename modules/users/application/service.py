from unicodedata import name

from modules.users.domain import User, IUnitOfWork


class UserService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow


    async def get_users(self):
        async with self.uow:
            return await self.uow.users.get()


    async def get_user_by_id(self, user_id: int):
        async with self.uow:
            user = await self.uow.users.get_by_id(user_id)
            
            if not user:
                raise Exception("User not found")
            
            return user
        
        
    async def create_user(self, username: str, email: str, password: str):
        async with self.uow:
            user = User(username=username, email=email, password=password)
            await self.uow.users.add(user)
            await self.uow.commit()
            return user
    
    
    async def update_user(self, user_id: int, username: str, email: str):
        async with self.uow:
            user = await self.uow.users.get_by_id(user_id)
            
            if not user:
                raise Exception("User not found")
            
            user.username = username
            user.email = email
            await self.uow.users.update(user)
            await self.uow.commit()
            return user
            

    async def delete_user(self, user_id: int):
        async with self.uow:
            user = await self.uow.users.get_by_id(user_id)
            
            if not user:
                raise Exception("User not found")
            
            await self.uow.users.delete(user)
            await self.uow.commit()
            return user