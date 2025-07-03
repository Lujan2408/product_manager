import pytest
from sqlmodel import select
from app.services.product_service import ProductService
from app.models.products.product import Product
from app.schemas.product import ProductCreate, ProductUpdate
from app.errors.product_errors import ProductNotFoundError, DuplicateProductNameError, NoFieldsToUpdateError
import asyncio

class TestProductService:
    """Test suite for ProductService class covering all business logic methods."""

    @pytest.mark.asyncio
    async def test_create_product_success(self, test_session, sample_product_data):
        """Test successful product creation with valid data."""
        # Arrange
        service = ProductService(test_session)
        product_data = ProductCreate(**sample_product_data)
        
        # Act
        created_product = await service.create_product(product_data)
        
        # Assert
        assert created_product is not None
        assert created_product.id is not None
        assert created_product.name == sample_product_data["name"]
        assert created_product.price == sample_product_data["price"]
        assert created_product.available == sample_product_data["available"]
        assert created_product.created_at is not None
        assert created_product.updated_at is not None

    @pytest.mark.asyncio
    async def test_create_product_duplicate_name_error(self, test_session, sample_product_data):
        """Test that creating a product with duplicate name raises DuplicateProductNameError."""
        # Arrange
        service = ProductService(test_session)
        product_data = ProductCreate(**sample_product_data)
        
        # Create first product
        await service.create_product(product_data)
        
        # Act & Assert - Try to create second product with same name
        with pytest.raises(DuplicateProductNameError) as exc_info:
            await service.create_product(product_data)
        
        assert f"Product with name {sample_product_data['name']} already exists" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_get_all_products_empty(self, test_session):
        """Test getting all products when database is empty."""
        # Arrange
        service = ProductService(test_session)
        
        # Act
        products = await service.get_all_products()
        
        # Assert
        assert products is not None
        assert len(products) == 0

    @pytest.mark.asyncio
    async def test_get_all_products_with_data(self, test_session, sample_product_data):
        """Test getting all products when database has products."""
        # Arrange
        service = ProductService(test_session)
        product_data = ProductCreate(**sample_product_data)
        
        # Create multiple products
        product1 = await service.create_product(product_data)
        
        # Create second product with different name
        product_data2 = ProductCreate(
            name="Another Product",
            price=150.0,
            available=False
        )
        product2 = await service.create_product(product_data2)
        
        # Act
        products = await service.get_all_products()
        
        # Assert
        assert len(products) == 2
        product_names = [p.name for p in products]
        assert sample_product_data["name"] in product_names
        assert "Another Product" in product_names

    @pytest.mark.asyncio
    async def test_get_product_by_id_success(self, test_session, sample_product_data):
        """Test successful product retrieval by ID."""
        # Arrange
        service = ProductService(test_session)
        product_data = ProductCreate(**sample_product_data)
        created_product = await service.create_product(product_data)
        
        # Act
        retrieved_product = await service.get_product_by_id(created_product.id)
        
        # Assert
        assert retrieved_product is not None
        assert retrieved_product.id == created_product.id
        assert retrieved_product.name == created_product.name
        assert retrieved_product.price == created_product.price
        assert retrieved_product.available == created_product.available

    @pytest.mark.asyncio
    async def test_get_product_by_id_not_found(self, test_session):
        """Test that getting non-existent product raises ProductNotFoundError."""
        # Arrange
        service = ProductService(test_session)
        non_existent_id = 999
        
        # Act & Assert
        with pytest.raises(ProductNotFoundError) as exc_info:
            await service.get_product_by_id(non_existent_id)
        
        assert "Product not found or does not exist" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_update_product_success_name_only(self, test_session, sample_product_data):
        """Test successful product update with only name field."""
        # Arrange
        service = ProductService(test_session)
        product_data = ProductCreate(**sample_product_data)
        created_product = await service.create_product(product_data)
        
        update_data = ProductUpdate(name="Updated Product Name")
        
        # Act
        updated_product = await service.update_product(created_product.id, update_data)
        
        # Assert
        assert updated_product.name == "Updated Product Name"
        assert updated_product.price == created_product.price  # Unchanged
        assert updated_product.available == created_product.available  # Unchanged
        assert updated_product.id == created_product.id

    @pytest.mark.asyncio
    async def test_update_product_success_price_only(self, test_session, sample_product_data):
        """Test successful product update with only price field."""
        # Arrange
        service = ProductService(test_session)
        product_data = ProductCreate(**sample_product_data)
        created_product = await service.create_product(product_data)
        
        update_data = ProductUpdate(price=200.0)
        
        # Act
        updated_product = await service.update_product(created_product.id, update_data)
        
        # Assert
        assert updated_product.price == 200.0
        assert updated_product.name == created_product.name  # Unchanged
        assert updated_product.available == created_product.available  # Unchanged

    @pytest.mark.asyncio
    async def test_update_product_success_available_only(self, test_session, sample_product_data):
        """Test successful product update with only available field."""
        # Arrange
        service = ProductService(test_session)
        product_data = ProductCreate(**sample_product_data)
        created_product = await service.create_product(product_data)
        
        update_data = ProductUpdate(available=False)
        
        # Act
        updated_product = await service.update_product(created_product.id, update_data)
        
        # Assert
        assert updated_product.available is False
        assert updated_product.name == created_product.name  # Unchanged
        assert updated_product.price == created_product.price  # Unchanged

    @pytest.mark.asyncio
    async def test_update_product_success_all_fields(self, test_session, sample_product_data):
        """Test successful product update with all fields."""
        # Arrange
        service = ProductService(test_session)
        product_data = ProductCreate(**sample_product_data)
        created_product = await service.create_product(product_data)
        
        update_data = ProductUpdate(
            name="Fully Updated Product",
            price=300.0,
            available=False
        )
        
        # Act
        updated_product = await service.update_product(created_product.id, update_data)
        
        # Assert
        assert updated_product.name == "Fully Updated Product"
        assert updated_product.price == 300.0
        assert updated_product.available is False

    @pytest.mark.asyncio
    async def test_update_product_not_found(self, test_session):
        """Test that updating non-existent product raises ProductNotFoundError."""
        # Arrange
        service = ProductService(test_session)
        non_existent_id = 999
        update_data = ProductUpdate(name="Updated Name")
        
        # Act & Assert
        with pytest.raises(ProductNotFoundError) as exc_info:
            await service.update_product(non_existent_id, update_data)
        
        assert "Product not found or does not exist" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_update_product_no_fields_provided(self, test_session, sample_product_data):
        """Test that updating with no fields raises NoFieldsToUpdateError."""
        # Arrange
        service = ProductService(test_session)
        product_data = ProductCreate(**sample_product_data)
        created_product = await service.create_product(product_data)
        
        update_data = ProductUpdate()  # No fields provided
        
        # Act & Assert
        with pytest.raises(NoFieldsToUpdateError) as exc_info:
            await service.update_product(created_product.id, update_data)
        
        assert "At least one field must be provided to update the product" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_update_product_duplicate_name_error(self, test_session, sample_product_data):
        """Test that updating with duplicate name raises DuplicateProductNameError."""
        # Arrange
        service = ProductService(test_session)
        
        # Create first product
        product_data1 = ProductCreate(**sample_product_data)
        product1 = await service.create_product(product_data1)
        
        # Create second product with different name
        product_data2 = ProductCreate(
            name="Second Product",
            price=150.0,
            available=True
        )
        product2 = await service.create_product(product_data2)
        
        # Try to update second product with first product's name
        update_data = ProductUpdate(name=sample_product_data["name"])
        
        # Act & Assert
        with pytest.raises(DuplicateProductNameError) as exc_info:
            await service.update_product(product2.id, update_data)
        
        assert f"Product with name {sample_product_data['name']} already exists" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_update_product_same_name_allowed(self, test_session, sample_product_data):
        """Test that updating with the same name is allowed (no duplicate error)."""
        # Arrange
        service = ProductService(test_session)
        product_data = ProductCreate(**sample_product_data)
        created_product = await service.create_product(product_data)
        
        # Update with same name
        update_data = ProductUpdate(name=sample_product_data["name"])
        
        # Act
        updated_product = await service.update_product(created_product.id, update_data)
        
        # Assert - Should not raise error and should update successfully
        assert updated_product.name == sample_product_data["name"]
        assert updated_product.id == created_product.id

    @pytest.mark.asyncio
    async def test_delete_product_success(self, test_session, sample_product_data):
        """Test successful product deletion."""
        # Arrange
        service = ProductService(test_session)
        product_data = ProductCreate(**sample_product_data)
        created_product = await service.create_product(product_data)
        
        # Act
        deleted_product = await service.delete_product(created_product.id)
        
        # Assert
        assert deleted_product is not None
        assert deleted_product.id == created_product.id
        
        # Verify product is actually deleted
        with pytest.raises(ProductNotFoundError):
            await service.get_product_by_id(created_product.id)

    @pytest.mark.asyncio
    async def test_delete_product_not_found(self, test_session):
        """Test that deleting non-existent product raises ProductNotFoundError."""
        # Arrange
        service = ProductService(test_session)
        non_existent_id = 999
        
        # Act & Assert
        with pytest.raises(ProductNotFoundError) as exc_info:
            await service.delete_product(non_existent_id)
        
        assert "Product not found or does not exist" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_product_created_at_updated_at_timestamps(self, test_session, sample_product_data):
        """Test that created_at and updated_at timestamps are set correctly."""
        # Arrange
        service = ProductService(test_session)
        product_data = ProductCreate(**sample_product_data)
        
        # Act
        created_product = await service.create_product(product_data)
        
        # Assert
        assert created_product.created_at is not None
        assert created_product.updated_at is not None
        assert created_product.created_at == created_product.updated_at  # Initially same

    @pytest.mark.asyncio
    async def test_product_updated_at_changes_on_update(self, test_session, sample_product_data):
        """Test that updated_at timestamp changes when product is updated."""
        # Arrange
        service = ProductService(test_session)
        product_data = ProductCreate(**sample_product_data)
        created_product = await service.create_product(product_data)
        original_updated_at = created_product.updated_at
        # Esperar un segundo para asegurar diferencia de timestamp
        await asyncio.sleep(1)
        # Act - Update the product
        update_data = ProductUpdate(name="Updated Name")
        updated_product = await service.update_product(created_product.id, update_data)
        # Assert
        assert updated_product.updated_at > original_updated_at
        assert updated_product.created_at == original_updated_at  # Should not change

    @pytest.mark.asyncio
    async def test_product_service_with_minimal_data(self, test_session, sample_product_data_minimal):
        """Test product service operations with minimal required data."""
        # Arrange
        service = ProductService(test_session)
        product_data = ProductCreate(**sample_product_data_minimal)
        
        # Act - Create
        created_product = await service.create_product(product_data)
        
        # Assert
        assert created_product.name == sample_product_data_minimal["name"]
        assert created_product.price == sample_product_data_minimal["price"]
        assert created_product.available == sample_product_data_minimal["available"]
        
        # Act - Get by ID
        retrieved_product = await service.get_product_by_id(created_product.id)
        assert retrieved_product.id == created_product.id
        
        # Act - Update
        update_data = ProductUpdate(price=75.0)
        updated_product = await service.update_product(created_product.id, update_data)
        assert updated_product.price == 75.0
        
        # Act - Delete
        deleted_product = await service.delete_product(created_product.id)
        assert deleted_product.id == created_product.id
        