from fastapi import Depends
# from sqlalchemy.orm import Session
import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db

from modules.users.infrastructure import PokeAPIClient, SQLAlchemyUnitOfWork
from modules.users.application.service import UserService


async def get_http_client():
    async with httpx.AsyncClient() as client:
        yield client


async def get_user_service(
    session: AsyncSession = Depends(get_db), 
    http_client: httpx.AsyncClient = Depends(get_http_client)
) -> UserService:
    uow = SQLAlchemyUnitOfWork(session)
    poke_gateway = PokeAPIClient(http_client)
    return UserService(uow, poke_gateway)