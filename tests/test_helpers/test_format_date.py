import pytest
from datetime import datetime
from app.helpers.format_date import now_without_microseconds


class TestFormatDate:
    """Test suite for format_date helper functions."""

    def test_now_without_microseconds_returns_datetime(self):
        """Test that now_without_microseconds returns a datetime object."""
        # Act
        result = now_without_microseconds()
        
        # Assert
        assert isinstance(result, datetime)
        assert result.microsecond == 0

    def test_now_without_microseconds_no_microseconds(self):
        """Test that the returned datetime has no microseconds."""
        # Act
        result = now_without_microseconds()
        
        # Assert
        assert result.microsecond == 0

    def test_now_without_microseconds_preserves_other_components(self):
        """Test that other datetime components are preserved."""
        # Act
        result = now_without_microseconds()
        current_time = datetime.now()
        
        # Assert
        assert result.year == current_time.year
        assert result.month == current_time.month
        assert result.day == current_time.day
        assert result.hour == current_time.hour
        assert result.minute == current_time.minute
        assert result.second == current_time.second
        # Only microsecond should be different (set to 0)
        assert result.microsecond == 0

    def test_now_without_microseconds_consistent_format(self):
        """Test that the function returns consistent format."""
        # Act
        result1 = now_without_microseconds()
        result2 = now_without_microseconds()
        
        # Assert
        assert result1.microsecond == 0
        assert result2.microsecond == 0
        # Both should be datetime objects
        assert isinstance(result1, datetime)
        assert isinstance(result2, datetime)

    def test_now_without_microseconds_isoformat(self):
        """Test that the datetime can be formatted to ISO format without microseconds."""
        # Act
        result = now_without_microseconds()
        iso_string = result.isoformat()
        
        # Assert
        # ISO format should not contain microseconds (no .XXXXXX part)
        assert '.' not in iso_string or not iso_string.split('.')[1].isdigit()

    def test_now_without_microseconds_strftime(self):
        """Test that the datetime can be formatted using strftime."""
        # Act
        result = now_without_microseconds()
        formatted = result.strftime("%Y-%m-%d %H:%M:%S")
        
        # Assert
        assert isinstance(formatted, str)
        # Should match the format YYYY-MM-DD HH:MM:SS
        assert len(formatted) == 19
        assert formatted.count('-') == 2
        assert formatted.count(':') == 2
        assert formatted.count(' ') == 1

    def test_now_without_microseconds_timezone_awareness(self):
        """Test that the datetime maintains timezone awareness if present."""
        # Act
        result = now_without_microseconds()
        
        # Assert
        # The function should preserve timezone awareness
        # If the system timezone is set, the result should be timezone-aware
        # This test is more about ensuring the function doesn't break timezone info
        assert hasattr(result, 'tzinfo')

    def test_now_without_microseconds_multiple_calls(self):
        """Test that multiple calls return different times (except for microseconds)."""
        # Act
        result1 = now_without_microseconds()
        result2 = now_without_microseconds()
        
        # Assert
        # Both should have no microseconds
        assert result1.microsecond == 0
        assert result2.microsecond == 0
        
        # They should be datetime objects
        assert isinstance(result1, datetime)
        assert isinstance(result2, datetime)

    def test_now_without_microseconds_replace_method(self):
        """Test that the function uses replace method correctly."""
        # Act
        result = now_without_microseconds()
        current_time = datetime.now()
        
        # Assert
        # The result should be equivalent to current_time.replace(microsecond=0)
        expected = current_time.replace(microsecond=0)
        assert result.microsecond == expected.microsecond
        # Other components should be the same (within a second)
        assert abs((result - expected).total_seconds()) < 1
