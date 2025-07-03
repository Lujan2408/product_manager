import pytest
from fastapi import status
from app.main import app
from app.core.db import get_async_session

class TestProductHandlers:
    """Test suite for product API handlers covering all HTTP endpoints."""

    @pytest.mark.asyncio
    async def test_create_product_endpoint_success(self, client, test_session, sample_product_data):
        """Test successful product creation via API endpoint."""
        # Arrange
        app.dependency_overrides[get_async_session] = lambda: test_session
        
        # Act
        response = await client.post("/api/v1/products/", json=sample_product_data)
        
        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["message"] == "Product created successfully"
        assert data["status"] == "success"
        assert "data" in data
        assert data["data"]["name"] == sample_product_data["name"]
        assert data["data"]["price"] == sample_product_data["price"]
        assert data["data"]["available"] == sample_product_data["available"]
        assert "id" in data["data"]
        assert "created_at" in data["data"]
        assert "updated_at" in data["data"]

    @pytest.mark.asyncio
    async def test_create_product_endpoint_duplicate_name(self, client, test_session, sample_product_data):
        """Test product creation with duplicate name returns 400 error."""
        # Arrange
        app.dependency_overrides[get_async_session] = lambda: test_session
        
        # Create first product
        await client.post("/api/v1/products/", json=sample_product_data)
        
        # Act - Try to create second product with same name
        response = await client.post("/api/v1/products/", json=sample_product_data)
        
        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        data = response.json()
        assert "detail" in data
        assert f"Product with name {sample_product_data['name']} already exists" in data["detail"]

    @pytest.mark.asyncio
    async def test_create_product_endpoint_invalid_data(self, client, test_session):
        """Test product creation with invalid data returns validation error."""
        # Arrange
        app.dependency_overrides[get_async_session] = lambda: test_session
        invalid_data = {
            "name": "",  # Empty name
            "price": -10,  # Negative price
            "available": True
        }
        
        # Act
        response = await client.post("/api/v1/products/", json=invalid_data)
        
        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.asyncio
    async def test_get_products_endpoint_empty(self, client, test_session):
        """Test getting all products when database is empty."""
        # Arrange
        app.dependency_overrides[get_async_session] = lambda: test_session
        
        # Act
        response = await client.get("/api/v1/products/")
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0

    @pytest.mark.asyncio
    async def test_get_products_endpoint_with_data(self, client, test_session, sample_product_data):
        """Test getting all products when database has products."""
        # Arrange
        app.dependency_overrides[get_async_session] = lambda: test_session
        
        # Create products
        await client.post("/api/v1/products/", json=sample_product_data)
        
        product_data2 = {
            "name": "Second Product",
            "price": 150.0,
            "available": False
        }
        await client.post("/api/v1/products/", json=product_data2)
        
        # Act
        response = await client.get("/api/v1/products/")
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 2
        
        product_names = [p["name"] for p in data]
        assert sample_product_data["name"] in product_names
        assert "Second Product" in product_names

    @pytest.mark.asyncio
    async def test_get_product_by_id_endpoint_success(self, client, test_session, sample_product_data):
        """Test successful product retrieval by ID via API endpoint."""
        # Arrange
        app.dependency_overrides[get_async_session] = lambda: test_session
        
        # Create product
        create_response = await client.post("/api/v1/products/", json=sample_product_data)
        created_product = create_response.json()["data"]
        
        # Act
        response = await client.get(f"/api/v1/products/{created_product['id']}")
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == created_product["id"]
        assert data["name"] == created_product["name"]
        assert data["price"] == created_product["price"]
        assert data["available"] == created_product["available"]

    @pytest.mark.asyncio
    async def test_get_product_by_id_endpoint_not_found(self, client, test_session):
        """Test getting non-existent product returns 404 error."""
        # Arrange
        app.dependency_overrides[get_async_session] = lambda: test_session
        non_existent_id = 999
        
        # Act
        response = await client.get(f"/api/v1/products/{non_existent_id}")
        
        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.json()
        assert "detail" in data
        assert "Product not found or does not exist" in data["detail"]

    @pytest.mark.asyncio
    async def test_update_product_endpoint_success(self, client, test_session, sample_product_data):
        """Test successful product update via API endpoint."""
        # Arrange
        app.dependency_overrides[get_async_session] = lambda: test_session
        
        # Create product
        create_response = await client.post("/api/v1/products/", json=sample_product_data)
        created_product = create_response.json()["data"]
        
        update_data = {
            "name": "Updated Product Name",
            "price": 200.0,
            "available": False
        }
        
        # Act
        response = await client.patch(f"/api/v1/products/{created_product['id']}", json=update_data)
        
        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["name"] == "Updated Product Name"
        assert data["price"] == 200.0
        assert data["available"] is False
        assert data["id"] == created_product["id"]

    @pytest.mark.asyncio
    async def test_update_product_endpoint_partial(self, client, test_session, sample_product_data):
        """Test successful partial product update via API endpoint."""
        # Arrange
        app.dependency_overrides[get_async_session] = lambda: test_session
        
        # Create product
        create_response = await client.post("/api/v1/products/", json=sample_product_data)
        created_product = create_response.json()["data"]
        
        update_data = {
            "name": "Only Name Updated"
        }
        
        # Act
        response = await client.patch(f"/api/v1/products/{created_product['id']}", json=update_data)
        
        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["name"] == "Only Name Updated"
        assert data["price"] == created_product["price"]  # Unchanged
        assert data["available"] == created_product["available"]  # Unchanged

    @pytest.mark.asyncio
    async def test_update_product_endpoint_not_found(self, client, test_session):
        """Test updating non-existent product returns 404 error."""
        # Arrange
        app.dependency_overrides[get_async_session] = lambda: test_session
        non_existent_id = 999
        update_data = {"name": "Updated Name"}
        
        # Act
        response = await client.patch(f"/api/v1/products/{non_existent_id}", json=update_data)
        
        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.json()
        assert "detail" in data
        assert "Product not found or does not exist" in data["detail"]

    @pytest.mark.asyncio
    async def test_update_product_endpoint_duplicate_name(self, client, test_session, sample_product_data):
        """Test updating with duplicate name returns 400 error."""
        # Arrange
        app.dependency_overrides[get_async_session] = lambda: test_session
        
        # Create first product
        await client.post("/api/v1/products/", json=sample_product_data)
        
        # Create second product
        product_data2 = {
            "name": "Second Product",
            "price": 150.0,
            "available": True
        }
        create_response2 = await client.post("/api/v1/products/", json=product_data2)
        product2 = create_response2.json()["data"]
        
        # Try to update second product with first product's name
        update_data = {"name": sample_product_data["name"]}
        
        # Act
        response = await client.patch(f"/api/v1/products/{product2['id']}", json=update_data)
        
        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        data = response.json()
        assert "detail" in data
        assert f"Product with name {sample_product_data['name']} already exists" in data["detail"]

    @pytest.mark.asyncio
    async def test_update_product_endpoint_no_fields(self, client, test_session, sample_product_data):
        """Test updating with no fields returns 400 error."""
        # Arrange
        app.dependency_overrides[get_async_session] = lambda: test_session
        
        # Create product
        create_response = await client.post("/api/v1/products/", json=sample_product_data)
        created_product = create_response.json()["data"]
        
        update_data = {}  # No fields provided
        
        # Act
        response = await client.patch(f"/api/v1/products/{created_product['id']}", json=update_data)
        
        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        data = response.json()
        assert "detail" in data
        assert "At least one field must be provided to update the product" in data["detail"]

    @pytest.mark.asyncio
    async def test_delete_product_endpoint_success(self, client, test_session, sample_product_data):
        """Test successful product deletion via API endpoint."""
        # Arrange
        app.dependency_overrides[get_async_session] = lambda: test_session
        
        # Create product
        create_response = await client.post("/api/v1/products/", json=sample_product_data)
        created_product = create_response.json()["data"]
        
        # Act
        response = await client.delete(f"/api/v1/products/{created_product['id']}")
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["message"] == f"Product with ID: {created_product['id']} deleted successfully"
        assert data["status"] == "success"
        
        # Verify product is actually deleted
        get_response = await client.get(f"/api/v1/products/{created_product['id']}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    async def test_delete_product_endpoint_not_found(self, client, test_session):
        """Test deleting non-existent product returns 404 error."""
        # Arrange
        app.dependency_overrides[get_async_session] = lambda: test_session
        non_existent_id = 999
        
        # Act
        response = await client.delete(f"/api/v1/products/{non_existent_id}")
        
        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.json()
        assert "detail" in data
        assert "Product not found or does not exist" in data["detail"]

    @pytest.mark.asyncio
    async def test_product_endpoints_http_methods(self, client, test_session):
        """Test that only appropriate HTTP methods are allowed for each endpoint."""
        # Arrange
        app.dependency_overrides[get_async_session] = lambda: test_session
        
        # Test products list endpoint
        response = await client.post("/api/v1/products/")
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY  # Missing body
        
        response = await client.put("/api/v1/products/")
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        
        response = await client.delete("/api/v1/products/")
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        
        # Test individual product endpoint
        response = await client.post("/api/v1/products/1")
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        
        response = await client.put("/api/v1/products/1")
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    @pytest.mark.asyncio
    async def test_product_endpoints_response_structure(self, client, test_session, sample_product_data):
        """Test that API responses have the correct structure."""
        # Arrange
        app.dependency_overrides[get_async_session] = lambda: test_session
        
        # Create product
        create_response = await client.post("/api/v1/products/", json=sample_product_data)
        created_product = create_response.json()["data"]
        
        # Test create response structure
        assert "message" in create_response.json()
        assert "data" in create_response.json()
        assert "status" in create_response.json()
        
        # Test get by ID response structure
        get_response = await client.get(f"/api/v1/products/{created_product['id']}")
        data = get_response.json()
        assert "id" in data
        assert "name" in data
        assert "price" in data
        assert "available" in data
        assert "created_at" in data
        assert "updated_at" in data
        
        # Test get all response structure
        get_all_response = await client.get("/api/v1/products/")
        data_list = get_all_response.json()
        assert isinstance(data_list, list)
        if len(data_list) > 0:
            assert "id" in data_list[0]
            assert "name" in data_list[0]
            assert "price" in data_list[0]
            assert "available" in data_list[0]

    def teardown_method(self):
        """Clean up dependency overrides after each test."""
        app.dependency_overrides.clear() 