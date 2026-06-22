from abc import ABC, abstractmethod
from typing import List
from .models import User

class IUserRepository(ABC):
    @abstractmethod
    async def get(self) -> List[User]:
        pass
    
    @abstractmethod
    async def get_by_id(self, user_id: int) -> User:
        pass

    @abstractmethod
    async def add(self, user: User):
        pass
    
    @abstractmethod
    async def update(self, user: User):
        pass
    
    @abstractmethod
    async def delete(self, user: User):
        pass