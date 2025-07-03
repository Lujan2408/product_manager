import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


class TestMainEndpoint:
    """
    Class that groups all tests related to the main endpoint.
    In pytest, classes that start with 'Test' are automatically executed.
    """
    
    @pytest.mark.asyncio  # ← ASYNC MARKER
    async def test_root_endpoint_returns_welcome_message(self):
        """
        Test that verifies the root endpoint returns the correct welcome message.
        """
        
        # ARRANGE (Prepare) - Set up the test environment
        # AsyncClient is an HTTP client that simulates real requests to your API
        transport = ASGITransport(app=app)  # ← Use ASGITransport instead of AsyncClient to avoid the error
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            
            # ACT (Act) - Execute the action we want to test
            # Make a GET request to the "/" endpoint
            response = await client.get("/")
            
            # ASSERT (Verify) - Check that the result is as expected
            # Verify that the status code is 200 (OK)
            assert response.status_code == 200
            
            # Verify that the response JSON has the correct structure
            data = response.json()
            assert "message" in data
            assert "status" in data
            assert data["message"] == "Welcome to Product Manager API"
            assert data["status"] == "running"
    
    @pytest.mark.asyncio
    async def test_root_endpoint_response_structure(self):
        """
        Test that verifies the complete structure of the root endpoint response.
        This test is more specific and verifies each field individually.
        """
        
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/")
            
            # Verify that the response is successful
            assert response.status_code == 200
            
            # Verify that the Content-Type is application/json
            assert response.headers["content-type"] == "application/json"
            
            # Verify the exact structure of the JSON
            expected_data = {
                "message": "Welcome to Product Manager API",
                "status": "running"
            }
            assert response.json() == expected_data
    
    @pytest.mark.asyncio
    async def test_root_endpoint_http_methods(self):
        """
        Test that verifies only the GET method works on the root endpoint.
        Other HTTP methods should return 405 Method Not Allowed.
        """
        
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            
            # GET should work (200 OK)
            response = await client.get("/")
            assert response.status_code == 200
            
            # POST should not work (405 Method Not Allowed)
            response = await client.post("/")
            assert response.status_code == 405
            
            # PUT should not work (405 Method Not Allowed)
            response = await client.put("/")
            assert response.status_code == 405
            
            # DELETE should not work (405 Method Not Allowed)
            response = await client.delete("/")
            assert response.status_code == 405


# ============================================================================
# KEY CONCEPTS EXPLANATION:
# ============================================================================

"""
1. @pytest.mark.asyncio:
   - This is a pytest "marker"
   - Tells pytest that this test is asynchronous
   - Without this, pytest wouldn't know how to execute async functions

2. async def test_...():
   - async: Indicates that the function is asynchronous
   - def: Defines a test function
   - test_...: pytest automatically looks for functions that start with "test_"

3. AsyncClient:
   - It's an HTTP client that simulates real requests
   - Allows making requests to your API without needing a real server
   - It's faster than using real requests

4. assert:
   - It's the keyword for making verifications
   - If the condition is False, the test fails
   - If it's True, the test passes

5. response.status_code:
   - HTTP status code (200=OK, 404=Not Found, etc.)
   - It's the standard way to verify if a request was successful

6. response.json():
   - Converts the JSON response into a Python dictionary
   - Allows verifying the content of the response

7. AAA Pattern (Arrange-Act-Assert):
   - Arrange: Prepare the test environment
   - Act: Execute the action we want to test
   - Assert: Verify that the result is as expected
""" 