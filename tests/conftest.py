import asyncio
from typing import AsyncGenerator
from httpx import AsyncClient
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel

# Importar tu aplicación
from app.main import app

# Configurar pytest-asyncio
pytest_plugins = ("pytest_asyncio",)

# ============================================================================
# FIXTURES DE EVENT LOOP
# ============================================================================

@pytest_asyncio.fixture(scope="function")
def event_loop():
    """
    Crear un event loop por cada test.
    """
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()

# ============================================================================
# FIXTURES DE BASE DE DATOS SQLITE
# ============================================================================

@pytest_asyncio.fixture
async def test_engine():
    """
    Crear un motor de base de datos SQLite para testing.
    Usa SQLite en memoria para máxima velocidad.
    """
    test_database_url = "sqlite+aiosqlite:///:memory:"
    
    engine = create_async_engine(
        test_database_url,
        echo=False,  # No mostrar SQL en consola durante tests
        poolclass=StaticPool,  # Pool estático para tests
        connect_args={"check_same_thread": False}
    )
    
    # Crear todas las tablas
    async with engine.begin() as conn:
        # Importar todos los modelos para crear las tablas
        from app.models.products.product import Product
        await conn.run_sync(SQLModel.metadata.create_all)
    
    yield engine  # ← DEVOLVER EL ENGINE, NO UN GENERADOR
    
    # Limpiar después de cada test
    await engine.dispose()

@pytest_asyncio.fixture
async def test_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """
    Crear una sesión de base de datos para cada test.
    """
    async_session = sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    
    async with async_session() as session:
        # Iniciar transacción anidada para rollback automático
        transaction = await session.begin_nested()
        
        yield session
        
        # Rollback automático después de cada test
        await transaction.rollback()
        await session.rollback()

# ============================================================================
# FIXTURES DE CLIENTE HTTP
# ============================================================================

@pytest_asyncio.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    """
    Cliente HTTP para hacer requests a tu API durante tests.
    """
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

# ============================================================================
# FIXTURES DE DATOS DE PRUEBA
# ============================================================================

@pytest_asyncio.fixture
def sample_product_data():
    """
    Datos de ejemplo para crear productos en tests.
    """
    return {
        "name": "Test Product",
        "description": "This is a test product",
        "price": 99.99
    }

@pytest_asyncio.fixture
def sample_product_data_invalid():
    """
    Datos inválidos para probar validaciones.
    """
    return {
        "name": "",  # Nombre vacío
        "price": -10,  # Precio negativo
    }

@pytest_asyncio.fixture
def sample_product_data_minimal():
    """
    Datos mínimos para crear un producto.
    """
    return {
        "name": "Minimal Product",
        "price": 50.0
    }

# ============================================================================
# FIXTURES DE UTILIDAD
# ============================================================================

@pytest_asyncio.fixture
def mock_time(mocker):
    """
    Mock para fechas y tiempos en tests.
    """
    mocker.patch("app.utils.format_date.datetime")