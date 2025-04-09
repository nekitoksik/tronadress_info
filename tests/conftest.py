import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.api.config import settings
from app.api.database import Base
from app.api.main import app
import asyncio

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def engine():
    engine = create_async_engine(f"{settings.DATABASE_URL}_test")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()

@pytest.fixture
async def session(engine):
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except:
            await session.rollback()
            raise
        finally:
            await session.close()

@pytest.fixture
def client():
    return TestClient(app)




































# import pytest
# from fastapi.testclient import TestClient
# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
# from sqlalchemy.orm import sessionmaker

# from app.api.config import settings
# from app.api.database import Base
# from app.api.main import app

# # @pytest.fixture
# # def mocker():
# #     from pytest_mock import MockerFixture
# #     return MockerFixture()

# @pytest.fixture
# def client():
#     return TestClient(app)




# @pytest.fixture(scope="session")
# async def engine():
#     engine = create_async_engine(f"{settings.DATABASE_URL}_test")
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#     yield engine
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)

# @pytest.fixture(scope="function")
# async def session(engine):
#     async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
#     async with async_session() as session:
#         yield session