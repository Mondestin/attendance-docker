from fastapi.testclient import TestClient
from main import app
import pytest

# Create a TestClient instance for making HTTP requests
client = TestClient(app)

# Test case for creating a user successfully
def test_create_user_success():
    # Make a POST request to the signup endpoint with valid user data
    res = client.post("/auth/signup", json={
        "email": "test.user1@gmail.com", "password": "password"
    })
    
    # Assert that the response status code is 201 (Created)
    assert res.status_code == 201

# Test case for creating a user with a conflicting email address
def test_create_user_conflict(create_user):
    # Use the same email address created by the create_user fixture
    conflicting_email = "test@gmail.com"
    
    # Make a POST request to the signup endpoint with conflicting user data
    res = client.post("/auth/signup", json={
        "email": conflicting_email, 'password': "password"
    })
    
    # Assert that the response status code is 409 (Conflict)
    assert res.status_code == 409
