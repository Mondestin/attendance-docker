from fastapi.testclient import TestClient
from main import app

# Create a TestClient instance
client = TestClient(app)

# Define a test for the main endpoint ("/") to check if the documentation is accessible
def test_docs():
    # Make a GET request to the root endpoint
    res = client.get("/docs")
    # Assert that the response status code is 200 (OK)
    assert res.status_code == 200

# Define a test for the Redoc documentation endpoint ("/redoc")
def test_redoc():
    # Make a GET request to the Redoc endpoint
    res = client.get("/redoc")
    # Assert that the response status code is 200 (OK)
    assert res.status_code == 200
