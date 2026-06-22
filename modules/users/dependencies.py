from fastapi import Depends
# from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from modules.users.infrastructure.sqlalchemy_unit_of_work import SQLAlchemyUnitOfWork
from modules.users.application.service import UserService


#def get_user_service(session: Session = Depends(get_db)) -> UserService:
async def get_user_service(session: AsyncSession = Depends(get_db)) -> UserService:
    uow = SQLAlchemyUnitOfWork(session)
    return UserService(uow)