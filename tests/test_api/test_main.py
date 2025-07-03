import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


class TestMainEndpoint:
    """
    Clase que agrupa todos los tests relacionados con el endpoint principal.
    En pytest, las clases que empiezan con 'Test' se ejecutan automáticamente.
    """
    
    @pytest.mark.asyncio  # ← MARCA ASÍNCRONA
    async def test_root_endpoint_returns_welcome_message(self):
        """
        Test que verifica que el endpoint raíz devuelve el mensaje de bienvenida correcto.
        
        NOMBRE DEL TEST: Debe ser descriptivo y explicar qué está probando
        """
        
        # ARRANGE (Preparar) - Configurar el entorno de prueba
        # AsyncClient es un cliente HTTP que simula requests reales a tu API
        transport = ASGITransport(app=app)  # ← Usar ASGITransport en lugar de AsyncClient para evitar el error
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            
            # ACT (Actuar) - Ejecutar la acción que queremos probar
            # Hacemos un GET request al endpoint "/"
            response = await client.get("/")
            
            # ASSERT (Verificar) - Comprobar que el resultado es el esperado
            # Verificamos que el status code sea 200 (OK)
            assert response.status_code == 200
            
            # Verificamos que el JSON de respuesta tenga la estructura correcta
            data = response.json()
            assert "message" in data
            assert "status" in data
            assert data["message"] == "Welcome to Product Manager API"
            assert data["status"] == "running"
    
    @pytest.mark.asyncio
    async def test_root_endpoint_response_structure(self):
        """
        Test que verifica la estructura completa de la respuesta del endpoint raíz.
        Este test es más específico y verifica cada campo individualmente.
        """
        
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/")
            
            # Verificamos que la respuesta sea exitosa
            assert response.status_code == 200
            
            # Verificamos que el Content-Type sea application/json
            assert response.headers["content-type"] == "application/json"
            
            # Verificamos la estructura exacta del JSON
            expected_data = {
                "message": "Welcome to Product Manager API",
                "status": "running"
            }
            assert response.json() == expected_data
    
    @pytest.mark.asyncio
    async def test_root_endpoint_http_methods(self):
        """
        Test que verifica que solo el método GET funciona en el endpoint raíz.
        Los otros métodos HTTP deberían devolver 405 Method Not Allowed.
        """
        
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            
            # GET debería funcionar (200 OK)
            response = await client.get("/")
            assert response.status_code == 200
            
            # POST no debería funcionar (405 Method Not Allowed)
            response = await client.post("/")
            assert response.status_code == 405
            
            # PUT no debería funcionar (405 Method Not Allowed)
            response = await client.put("/")
            assert response.status_code == 405
            
            # DELETE no debería funcionar (405 Method Not Allowed)
            response = await client.delete("/")
            assert response.status_code == 405


# ============================================================================
# EXPLICACIÓN DE CONCEPTOS CLAVE:
# ============================================================================

"""
1. @pytest.mark.asyncio:
   - Esta es una "marca" (marker) de pytest
   - Le dice a pytest que este test es asíncrono
   - Sin esto, pytest no sabría cómo ejecutar funciones async

2. async def test_...():
   - async: Indica que la función es asíncrona
   - def: Define una función de test
   - test_...: pytest busca automáticamente funciones que empiecen con "test_"

3. AsyncClient:
   - Es un cliente HTTP que simula requests reales
   - Permite hacer requests a tu API sin necesidad de un servidor real
   - Es más rápido que usar requests reales

4. assert:
   - Es la palabra clave para hacer verificaciones
   - Si la condición es False, el test falla
   - Si es True, el test pasa

5. response.status_code:
   - Código de estado HTTP (200=OK, 404=Not Found, etc.)
   - Es la forma estándar de verificar si un request fue exitoso

6. response.json():
   - Convierte la respuesta JSON en un diccionario de Python
   - Permite verificar el contenido de la respuesta

7. Patrón AAA (Arrange-Act-Assert):
   - Arrange: Preparar el entorno de prueba
   - Act: Ejecutar la acción que queremos probar
   - Assert: Verificar que el resultado es el esperado
""" 