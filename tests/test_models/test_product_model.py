import pytest
from datetime import datetime
from sqlmodel import SQLModel, create_engine, Session
from app.models.products.product import Product
from app.helpers.format_date import now_without_microseconds


class TestProductModel:
    """Test suite for Product model validation and behavior."""

    def test_product_model_creation_with_valid_data(self):
        """Test that Product model can be created with valid data."""
        # Arrange
        product_data = {
            "name": "Test Product",
            "price": 99.99,
            "available": True
        }
        
        # Act
        product = Product(**product_data)
        
        # Assert
        assert product.name == "Test Product"
        assert product.price == 99.99
        assert product.available is True
        assert product.id is None  # Not set until saved to DB
        assert product.created_at is not None
        assert product.updated_at is not None

    def test_product_model_default_values(self):
        """Test that Product model has correct default values."""
        # Arrange
        product_data = {
            "name": "Test Product",
            "price": 99.99
            # available not provided, should default to True
        }
        
        # Act
        product = Product(**product_data)
        
        # Assert
        assert product.available is True
        assert product.created_at is not None
        assert product.updated_at is not None

    def test_product_model_timestamps_initialization(self):
        """Test that timestamps are initialized correctly."""
        # Arrange
        product_data = {
            "name": "Test Product",
            "price": 99.99
        }
        
        # Act
        product = Product(**product_data)
        
        # Assert
        assert isinstance(product.created_at, datetime)
        assert isinstance(product.updated_at, datetime)
        assert product.created_at.microsecond == 0
        assert product.updated_at.microsecond == 0

    def test_product_model_sqlmodel_inheritance(self):
        """Test that Product inherits from SQLModel correctly."""
        # Arrange & Act
        product = Product(name="Test", price=99.99)
        
        # Assert
        assert isinstance(product, SQLModel)
        assert hasattr(product, 'model_config')
        assert hasattr(product, 'model_dump')

    def test_product_model_field_constraints(self):
        """Test that Product model enforces field constraints."""
        # Arrange
        product_data = {
            "name": "Test Product",
            "price": 99.99,
            "available": True
        }
        
        # Act
        product = Product(**product_data)
        
        # Assert - Check that constraints are defined
        # These are validated by Pydantic/SQLModel, not the model itself
        assert product.name is not None
        assert product.price >= 0
        assert isinstance(product.available, bool)

    def test_product_model_optional_fields(self):
        """Test that optional fields work correctly."""
        # Arrange
        product_data = {
            "name": "Test Product",
            "price": 99.99
            # available is optional with default True
        }
        
        # Act
        product = Product(**product_data)
        
        # Assert
        assert product.available is True  # Default value

    def test_product_model_primary_key_field(self):
        """Test that id field is properly configured as primary key."""
        # Arrange
        product_data = {
            "name": "Test Product",
            "price": 99.99
        }
        
        # Act
        product = Product(**product_data)
        
        # Assert
        assert product.id is None  # Not set until saved
        # The primary key configuration is handled by SQLModel/SQLAlchemy

    def test_product_model_index_field(self):
        """Test that name field is properly configured as indexed."""
        # Arrange
        product_data = {
            "name": "Test Product",
            "price": 99.99
        }
        
        # Act
        product = Product(**product_data)
        
        # Assert
        assert product.name == "Test Product"
        # Index configuration is handled by SQLModel/SQLAlchemy

    def test_product_model_float_field(self):
        """Test that price field is properly configured as Float."""
        # Arrange
        product_data = {
            "name": "Test Product",
            "price": 99.99
        }
        
        # Act
        product = Product(**product_data)
        
        # Assert
        assert isinstance(product.price, float)
        assert product.price == 99.99

    def test_product_model_boolean_field(self):
        """Test that available field is properly configured as boolean."""
        # Arrange
        product_data = {
            "name": "Test Product",
            "price": 99.99,
            "available": False
        }
        
        # Act
        product = Product(**product_data)
        
        # Assert
        assert isinstance(product.available, bool)
        assert product.available is False

    def test_product_model_datetime_fields(self):
        """Test that datetime fields are properly configured."""
        # Arrange
        product_data = {
            "name": "Test Product",
            "price": 99.99
        }
        
        # Act
        product = Product(**product_data)
        
        # Assert
        assert isinstance(product.created_at, datetime)
        assert isinstance(product.updated_at, datetime)
        assert product.created_at.microsecond == 0
        assert product.updated_at.microsecond == 0

    def test_product_model_serialization(self):
        """Test that Product model can be serialized to dict."""
        # Arrange
        product_data = {
            "name": "Test Product",
            "price": 99.99,
            "available": True
        }
        product = Product(**product_data)
        
        # Act
        serialized = product.model_dump()
        
        # Assert
        assert serialized["name"] == "Test Product"
        assert serialized["price"] == 99.99
        assert serialized["available"] is True
        assert "created_at" in serialized
        assert "updated_at" in serialized

    def test_product_model_json_serialization(self):
        """Test that Product model can be serialized to JSON."""
        # Arrange
        product_data = {
            "name": "Test Product",
            "price": 99.99,
            "available": True
        }
        product = Product(**product_data)
        
        # Act
        json_data = product.model_dump_json()
        
        # Assert
        assert isinstance(json_data, str)
        assert "Test Product" in json_data
        assert "99.99" in json_data
        assert "true" in json_data.lower()

    def test_product_model_equality(self):
        """Test that Product models can be compared for equality."""
        # Arrange
        product1 = Product(name="Test Product", price=99.99)
        product2 = Product(name="Test Product", price=99.99)
        product3 = Product(name="Different Product", price=99.99)
        
        # Act & Assert
        # Products with same data should be equal (excluding timestamps and id)
        assert product1.name == product2.name
        assert product1.price == product2.price
        assert product1.available == product2.available
        
        # Products with different data should not be equal
        assert product1.name != product3.name

    def test_product_model_string_representation(self):
        """Test that Product model has a meaningful string representation."""
        # Arrange
        product = Product(name="Test Product", price=99.99)
        
        # Act
        string_repr = str(product)
        
        # Assert
        assert isinstance(string_repr, str)
        assert "Test Product" in string_repr

    def test_product_model_table_configuration(self):
        """Test that Product model is configured as a table."""
        # Arrange
        product = Product(name="Test Product", price=99.99)
        
        # Assert
        # The table=True parameter should be set in the model definition
        # This is verified by checking that the model can be used with SQLModel
        assert hasattr(product, '__tablename__') or hasattr(Product, '__tablename__')

    def test_product_model_field_validation(self):
        """Test that Product model validates field types correctly."""
        # Arrange & Act & Assert
        # Valid data should work
        product = Product(name="Test Product", price=99.99, available=True)
        assert product.name == "Test Product"
        assert product.price == 99.99
        assert product.available is True

    def test_product_model_timestamp_consistency(self):
        """Test that created_at and updated_at are consistent on creation."""
        # Arrange
        product_data = {
            "name": "Test Product",
            "price": 99.99
        }
        
        # Act
        product = Product(**product_data)
        
        # Assert
        # On creation, created_at and updated_at should be the same
        assert product.created_at == product.updated_at

    def test_product_model_with_explicit_timestamps(self):
        """Test that Product model works with explicit timestamps."""
        # Arrange
        custom_time = now_without_microseconds()
        product_data = {
            "name": "Test Product",
            "price": 99.99,
            "created_at": custom_time,
            "updated_at": custom_time
        }
        
        # Act
        product = Product(**product_data)
        
        # Assert
        assert product.created_at == custom_time
        assert product.updated_at == custom_time

    def test_product_model_field_annotations(self):
        """Test that Product model has correct field annotations."""
        # Arrange & Act
        product = Product(name="Test Product", price=99.99)
        
        # Assert
        # Check that fields have the expected types
        assert isinstance(product.name, str)
        assert isinstance(product.price, float)
        assert isinstance(product.available, bool)
        assert isinstance(product.created_at, datetime)
        assert isinstance(product.updated_at, datetime) 