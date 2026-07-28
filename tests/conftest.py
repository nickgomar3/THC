import os
from collections.abc import AsyncGenerator

from modules.users.infrastructure.poke_api import PokeAPIClient
from modules.users.application.service import UserService
from modules.users.infrastructure.sqlalchemy_unit_of_work import SQLAlchemyUnitOfWork
from .factories import UserFactory, UserPokemonFactory


os.environ["DATABASE_URL"] = (
    "postgresql+psycopg://challengeuser:challpass@db/test_thchallenge"
)


import pytest
import respx
import httpx
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from modules.users.dependencies import get_http_client, get_user_service
from core.database import Base, get_db
from core.config import settings
from main import app

import sys
import asyncio


pytest_plugins = ["anyio"]


# Windows Fix: Set appropriate event loop policy to avoid asyncio errors on Windows
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

@pytest.fixture(scope="session")
def event_loop():
    if sys.platform == "win32":
        """Explicitly creates an instance of the event loop for the test session."""
        loop = asyncio.new_event_loop()
        yield loop
        loop.close()
    else:
        # For Linux and macOS, the default event loop policy is sufficient
        loop = asyncio.get_event_loop_policy().new_event_loop()
        yield loop
        loop.close()
# End Windows Fix


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(autouse=True)
def mock_pokeapi():
    with respx.mock(base_url=settings.pokeapi_url, assert_all_mocked=False) as respx_mock:
        yield respx_mock


@pytest.fixture(scope="session")
def test_engine():
    engine = create_async_engine(
        os.environ["DATABASE_URL"],
        poolclass=NullPool,
    )
    return engine


@pytest.fixture(scope="session")
async def setup_database(test_engine):
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await test_engine.dispose()


@pytest.fixture
async def db_session(
    test_engine,
    setup_database,
) -> AsyncGenerator[AsyncSession]:
    conn = await test_engine.connect()
    trans = await conn.begin()

    test_async_session = async_sessionmaker(
        bind=conn,
        class_=AsyncSession,
        expire_on_commit=False,
        join_transaction_mode="create_savepoint",
    )

    async with test_async_session() as session:
        try:
            yield session
        finally:
            await session.close()
            await trans.rollback()
            await conn.close()


@pytest.fixture
async def client(
    db_session: AsyncSession
) -> AsyncGenerator[AsyncClient]:

    # 1. Creamos el override del servicio usando la sesión del test actual
    async def override_get_user_service():
        uow = SQLAlchemyUnitOfWork(db_session)
        # Le pasamos un AsyncClient de httpx para que cumpla con el __init__
        async_client = httpx.AsyncClient(base_url=settings.pokeapi_url)
        gateway = PokeAPIClient(client=async_client)
        return UserService(uow=uow, poke_gateway=gateway)

    async def override_get_db():
        yield db_session
    
    async def override_get_http_client():
        async with httpx.AsyncClient(base_url=settings.pokeapi_url) as ac:
            yield ac

    # 2. Aplicamos los overrides en FastAPI
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_http_client] = override_get_http_client
    app.dependency_overrides[get_user_service] = override_get_user_service
    
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac

    # 3. Limpiamos los overrides al terminar
    app.dependency_overrides.clear()


@pytest.fixture(autouse=True)
def set_factory_session(db_session):
    """Inyecta automáticamente la sesión de test en las factorías de SQLAlchemy."""
    UserFactory._meta.sqlalchemy_session = db_session
    UserPokemonFactory._meta.sqlalchemy_session = db_session