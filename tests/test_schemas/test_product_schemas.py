import pytest
from datetime import datetime
from pydantic import ValidationError
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate


class TestProductCreateSchema:
    """Test suite for ProductCreate schema validation."""

    def test_valid_product_create(self):
        """Test that valid product data passes validation."""
        # Arrange
        valid_data = {
            "name": "Test Product",
            "price": 99.99,
            "available": True
        }
        
        # Act
        product = ProductCreate(**valid_data)
        
        # Assert
        assert product.name == "Test Product"
        assert product.price == 99.99
        assert product.available is True

    def test_product_create_with_default_available(self):
        """Test that available field defaults to True when not provided."""
        # Arrange
        data_without_available = {
            "name": "Test Product",
            "price": 99.99
        }
        
        # Act
        product = ProductCreate(**data_without_available)
        
        # Assert
        assert product.available is True

    def test_product_create_empty_name_validation(self):
        """Test that empty name raises validation error."""
        # Arrange & Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            ProductCreate(name="", price=99.99)
        
        errors = exc_info.value.errors()
        assert len(errors) > 0
        assert any("String should have at least 1 character" in str(error) for error in errors)

    def test_product_create_name_too_long_validation(self):
        """Test that name longer than 255 characters raises validation error."""
        # Arrange
        long_name = "a" * 256
        
        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            ProductCreate(name=long_name, price=99.99)
        
        errors = exc_info.value.errors()
        assert len(errors) > 0
        assert any("String should have at most 255 characters" in str(error) for error in errors)

    def test_product_create_negative_price_validation(self):
        """Test that negative price raises validation error."""
        # Arrange & Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            ProductCreate(name="Test Product", price=-10.0)
        
        errors = exc_info.value.errors()
        assert len(errors) > 0
        assert any("Input should be greater than 0" in str(error) for error in errors)

    def test_product_create_zero_price_validation(self):
        """Test that zero price raises validation error."""
        # Arrange & Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            ProductCreate(name="Test Product", price=0.0)
        
        errors = exc_info.value.errors()
        assert len(errors) > 0
        assert any("Input should be greater than 0" in str(error) for error in errors)

    def test_product_create_missing_required_fields(self):
        """Test that missing required fields raise validation error."""
        # Arrange & Act & Assert - Missing name
        with pytest.raises(ValidationError) as exc_info:
            ProductCreate(price=99.99)
        
        errors = exc_info.value.errors()
        assert len(errors) > 0
        assert any("Field required" in str(error) for error in errors)
        
        # Arrange & Act & Assert - Missing price
        with pytest.raises(ValidationError) as exc_info:
            ProductCreate(name="Test Product")
        
        errors = exc_info.value.errors()
        assert len(errors) > 0
        assert any("Field required" in str(error) for error in errors)

    def test_product_create_invalid_price_type(self):
        """Test that invalid price type raises validation error."""
        # Arrange & Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            ProductCreate(name="Test Product", price="not_a_number")
        
        errors = exc_info.value.errors()
        assert len(errors) > 0
        assert any("Input should be a valid number" in str(error) for error in errors)

    def test_product_create_invalid_available_type(self):
        """Test that invalid available type raises validation error."""
        # Arrange & Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            ProductCreate(name="Test Product", price=99.99, available="not_boolean")
        
        errors = exc_info.value.errors()
        assert len(errors) > 0
        assert any("Input should be a valid boolean" in str(error) for error in errors)


class TestProductResponseSchema:
    """Test suite for ProductResponse schema validation."""

    def test_valid_product_response(self):
        """Test that valid product response data passes validation."""
        # Arrange
        valid_data = {
            "id": 1,
            "name": "Test Product",
            "price": 99.99,
            "available": True,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        # Act
        product = ProductResponse(**valid_data)
        
        # Assert
        assert product.id == 1
        assert product.name == "Test Product"
        assert product.price == 99.99
        assert product.available is True
        assert isinstance(product.created_at, datetime)
        assert isinstance(product.updated_at, datetime)

    def test_product_response_missing_required_fields(self):
        """Test that missing required fields raise validation error."""
        # Arrange & Act & Assert - Missing id
        with pytest.raises(ValidationError) as exc_info:
            ProductResponse(
                name="Test Product",
                price=99.99,
                available=True,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
        
        errors = exc_info.value.errors()
        assert len(errors) > 0
        assert any("Field required" in str(error) for error in errors)

    def test_product_response_invalid_id_type(self):
        """Test that invalid id type raises validation error."""
        # Arrange & Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            ProductResponse(
                id="not_an_integer",
                name="Test Product",
                price=99.99,
                available=True,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
        
        errors = exc_info.value.errors()
        assert len(errors) > 0
        assert any("Input should be a valid integer" in str(error) for error in errors)

    def test_product_response_invalid_datetime_type(self):
        """Test that invalid datetime type raises validation error."""
        # Arrange & Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            ProductResponse(
                id=1,
                name="Test Product",
                price=99.99,
                available=True,
                created_at="not_a_datetime",
                updated_at=datetime.now()
            )
        
        errors = exc_info.value.errors()
        assert len(errors) > 0
        assert any("Input should be a valid datetime" in str(error) for error in errors)


class TestProductUpdateSchema:
    """Test suite for ProductUpdate schema validation."""

    def test_valid_product_update_all_fields(self):
        """Test that valid product update data with all fields passes validation."""
        # Arrange
        valid_data = {
            "name": "Updated Product",
            "price": 150.0,
            "available": False
        }
        
        # Act
        product = ProductUpdate(**valid_data)
        
        # Assert
        assert product.name == "Updated Product"
        assert product.price == 150.0
        assert product.available is False

    def test_valid_product_update_partial_fields(self):
        """Test that valid product update data with partial fields passes validation."""
        # Arrange
        valid_data = {
            "name": "Updated Product"
        }
        
        # Act
        product = ProductUpdate(**valid_data)
        
        # Assert
        assert product.name == "Updated Product"
        assert product.price is None
        assert product.available is None

    def test_valid_product_update_empty_dict(self):
        """Test that empty dict creates ProductUpdate with all None values."""
        # Arrange & Act
        product = ProductUpdate()
        
        # Assert
        assert product.name is None
        assert product.price is None
        assert product.available is None

    def test_product_update_empty_name_validation(self):
        """Test that empty name raises validation error."""
        # Arrange & Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            ProductUpdate(name="")
        
        errors = exc_info.value.errors()
        assert len(errors) > 0
        assert any("String should have at least 1 character" in str(error) for error in errors)

    def test_product_update_name_too_long_validation(self):
        """Test that name longer than 255 characters raises validation error."""
        # Arrange
        long_name = "a" * 256
        
        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            ProductUpdate(name=long_name)
        
        errors = exc_info.value.errors()
        assert len(errors) > 0
        assert any("String should have at most 255 characters" in str(error) for error in errors)

    def test_product_update_negative_price_validation(self):
        """Test that negative price raises validation error."""
        # Arrange & Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            ProductUpdate(price=-10.0)
        
        errors = exc_info.value.errors()
        assert len(errors) > 0
        assert any("Input should be greater than 0" in str(error) for error in errors)

    def test_product_update_zero_price_validation(self):
        """Test that zero price raises validation error."""
        # Arrange & Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            ProductUpdate(price=0.0)
        
        errors = exc_info.value.errors()
        assert len(errors) > 0
        assert any("Input should be greater than 0" in str(error) for error in errors)

    def test_product_update_invalid_price_type(self):
        """Test that invalid price type raises validation error."""
        # Arrange & Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            ProductUpdate(price="not_a_number")
        
        errors = exc_info.value.errors()
        assert len(errors) > 0
        assert any("Input should be a valid number" in str(error) for error in errors)

    def test_product_update_invalid_available_type(self):
        """Test that invalid available type raises validation error."""
        # Arrange & Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            ProductUpdate(available="not_boolean")
        
        errors = exc_info.value.errors()
        assert len(errors) > 0
        assert any("Input should be a valid boolean" in str(error) for error in errors)

    def test_product_update_name_with_blank_spaces_validation(self):
        """Test that name with only blank spaces raises validation error."""
        # Arrange & Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            ProductUpdate(name="   ")
        
        errors = exc_info.value.errors()
        assert len(errors) > 0
        assert any("Name cannot be blank" in str(error) for error in errors)

    def test_product_update_name_with_leading_trailing_spaces(self):
        """Test that name with leading/trailing spaces is trimmed."""
        # Arrange
        name_with_spaces = "  Test Product  "
        
        # Act
        product = ProductUpdate(name=name_with_spaces)
        
        # Assert
        assert product.name == "Test Product"

    def test_product_update_name_with_internal_spaces(self):
        """Test that name with internal spaces is allowed."""
        # Arrange
        name_with_internal_spaces = "Test Product Name"
        
        # Act
        product = ProductUpdate(name=name_with_internal_spaces)
        
        # Assert
        assert product.name == "Test Product Name"


class TestProductSchemaIntegration:
    """Test suite for integration between different product schemas."""

    def test_create_to_response_conversion(self):
        """Test conversion from ProductCreate to ProductResponse."""
        # Arrange
        create_data = {
            "name": "Test Product",
            "price": 99.99,
            "available": True
        }
        create_schema = ProductCreate(**create_data)
        
        # Simulate response data (as if from database)
        response_data = {
            "id": 1,
            "name": create_schema.name,
            "price": create_schema.price,
            "available": create_schema.available,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        # Act
        response_schema = ProductResponse(**response_data)
        
        # Assert
        assert response_schema.name == create_schema.name
        assert response_schema.price == create_schema.price
        assert response_schema.available == create_schema.available

    def test_update_partial_fields(self):
        """Test that ProductUpdate allows partial updates."""
        # Arrange
        original_data = {
            "name": "Original Product",
            "price": 100.0,
            "available": True
        }
        
        update_data = {
            "price": 150.0
        }
        
        # Act
        update_schema = ProductUpdate(**update_data)
        
        # Assert
        assert update_schema.name is None
        assert update_schema.price == 150.0
        assert update_schema.available is None

    def test_schema_serialization(self):
        """Test that schemas can be serialized to dict."""
        # Arrange
        create_data = {
            "name": "Test Product",
            "price": 99.99,
            "available": True
        }
        
        # Act
        create_schema = ProductCreate(**create_data)
        serialized = create_schema.model_dump()
        
        # Assert
        assert serialized["name"] == "Test Product"
        assert serialized["price"] == 99.99
        assert serialized["available"] is True

    def test_schema_with_from_attributes(self):
        """Test that ProductResponse works with from_attributes=True."""
        # Arrange
        class MockProduct:
            def __init__(self):
                self.id = 1
                self.name = "Test Product"
                self.price = 99.99
                self.available = True
                self.created_at = datetime.now()
                self.updated_at = datetime.now()
        
        mock_product = MockProduct()
        
        # Act
        response_schema = ProductResponse.model_validate(mock_product)
        
        # Assert
        assert response_schema.id == 1
        assert response_schema.name == "Test Product"
        assert response_schema.price == 99.99
        assert response_schema.available is True 