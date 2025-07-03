import asyncio
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel

# Import your application
from app.main import app

# Configure pytest-asyncio
pytest_plugins = ("pytest_asyncio",)

# ============================================================================
# EVENT LOOP FIXTURES
# ============================================================================

@pytest_asyncio.fixture(scope="function")
def event_loop():
    """
    Create an event loop for each test.
    """
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()

# ============================================================================
# SQLITE DATABASE FIXTURES
# ============================================================================

@pytest_asyncio.fixture
async def test_engine():
    """
    Create a SQLite database engine for testing.
    Uses in-memory SQLite for maximum speed.
    """
    test_database_url = "sqlite+aiosqlite:///:memory:"
    
    engine = create_async_engine(
        test_database_url,
        echo=False,  # Don't show SQL in console during tests
        poolclass=StaticPool,  # Static pool for tests
        connect_args={"check_same_thread": False}
    )
    
    # Create all tables
    async with engine.begin() as conn:
        # Import all models to create tables
        from app.models.products.product import Product
        await conn.run_sync(SQLModel.metadata.create_all)
    
    yield engine  # ← RETURN THE ENGINE, NOT A GENERATOR
    
    # Clean up after each test
    await engine.dispose()

@pytest_asyncio.fixture
async def test_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """
    Create a database session for each test.
    """
    async_session = sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    
    async with async_session() as session:
        # Start transaction for automatic rollback
        await session.begin()
        
        yield session
        
        # Automatic rollback after each test (only if transaction is active)
        try:
            if session.in_transaction():
                await session.rollback()
        except Exception:
            # If already closed, do nothing
            pass

# ============================================================================
# HTTP CLIENT FIXTURES
# ============================================================================

@pytest_asyncio.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    """
    HTTP client to make requests to the API during tests.
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

# ============================================================================
# TEST DATA FIXTURES
# ============================================================================

@pytest_asyncio.fixture
def sample_product_data():
    """
    Sample data to create products in tests.
    """
    return {
        "name": "Test Product",
        "price": 99.99,
        "available": True
    }

@pytest_asyncio.fixture
def sample_product_data_invalid():
    """
    Invalid data to test validations.
    """
    return {
        "name": "",  # Empty name
        "price": -10,  # Negative price
        "available": False
    }

@pytest_asyncio.fixture
def sample_product_data_minimal():
    """
    Minimal data to create a product.
    """
    return {
        "name": "Minimal Product",
        "price": 50.0,
        "available": True
    }

# ============================================================================
# UTILITY FIXTURES
# ============================================================================

@pytest_asyncio.fixture
def mock_time(mocker):
    """
    Mock for dates and times in tests.
    """
    mocker.patch("app.utils.format_date.datetime")