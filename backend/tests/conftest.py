"""Shared test fixtures for the Todo application tests."""

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.database import Base, get_db
from app.main import app
from app.models.todo import Todo

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture()
async def engine():
    """Create an async test engine with in-memory SQLite."""
    test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield test_engine
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await test_engine.dispose()


@pytest.fixture()
async def session(engine):
    """Yield an async session for each test, rolled back after use."""
    async_session = async_sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as sess:
        yield sess


@pytest.fixture()
async def client(engine):
    """Yield an httpx AsyncClient wired to the test database."""
    async_session = async_sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )

    async def override_get_db():
        async with async_session() as sess:
            try:
                yield sess
                await sess.commit()
            except Exception:
                await sess.rollback()
                raise

    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest.fixture()
async def sample_todo(session) -> Todo:
    """Create and return a sample todo for testing."""
    todo = Todo(title="Test Todo", description="Test description")
    session.add(todo)
    await session.commit()
    await session.refresh(todo)
    return todo
