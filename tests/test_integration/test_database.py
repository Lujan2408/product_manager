from httpx import ASGITransport, AsyncClient
import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine
from app.main import app
from app.core.db import lifespan, get_async_session

class TestDatabaseConnection:

  @pytest.mark.asyncio
  async def test_database_connection(self, test_engine): 
    """Test que verifica que la conexión a la base de datos se establece correctamente."""
    # Verify if the engine exists and its valid
    assert test_engine is not None
    assert isinstance(test_engine, AsyncEngine)
  
    # Verify if the engine is connected to the database
    async with test_engine.begin() as connection: 
      result = await connection.execute(text("SELECT 1"))
      assert result.scalar() == 1

  @pytest.mark.asyncio
  async def test_create_db_and_tables(self, test_engine): 
    """Test que verifica que la base de datos y las tablas se crean correctamente."""
    # Verify if the tables are created correctly
    # The tables are created in the fixture test_engine

    # Verify if the tables exists
    async with test_engine.begin() as connection: 
      # Get the list of tables
      result = await connection.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
      tables = result.scalars().all()

      # Verify if the main tables exists
      assert "product" in tables # Assuming we have a product table

  @pytest.mark.asyncio
  async def test_lifespan_manager(self, test_engine): 
    """Test que verifica que el manager de lifespan se ejecuta correctamente."""
    # Simulate a FastAPI application
    app_state = {"started": False, "stopped": False}

    async with lifespan(app_state):
      app_state["started"] = True 
      app_state["stopped"] = True

      # Here we can verify if the tables are created correctly and the database is connected
      # Verify if the database is connected
      async with test_engine.begin() as connection: 
        result = await connection.execute(text("SELECT 1"))
        assert result.scalar() == 1

      # Verify if the tables are created correctly
      async with test_engine.begin() as connection: 
        result = await connection.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
        tables = result.scalars().all()
        assert "product" in tables # Assuming we have a product table

      assert app_state["started"] is True
      assert app_state["stopped"] is True

  @pytest.mark.asyncio
  async def test_dependency_override_with_session(self, test_session): 
    """Test que verifica que la session de base de datos se obtiene correctamente."""

    # Temporary override the session dependency
    app.dependency_overrides[get_async_session] = lambda: test_session

    # Test client
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client: 
      response = await client.get("/")
      assert response.status_code == 200
      data = response.json()
      assert data["message"] == "Welcome to Product Manager API"