from firebase_admin import auth
from fastapi.testclient import TestClient
from main import app
import pytest

# Set the TESTING environment variable to 'True'
import os
os.environ['TESTING'] = 'True'

# Create a TestClient instance
client = TestClient(app)

# Define a fixture to clean up resources after testing
@pytest.fixture(scope="session", autouse=True)
def cleanup(request):
    # Define a function to remove test users from Firebase
    def remove_test_users():
        users = auth.list_users().iterate_all()
        for user in users:
            if user.email.startswith("test."):
                auth.delete_user(user.uid)
    # Add the cleanup function to the finalizer, ensuring it runs after all tests
    request.addfinalizer(remove_test_users)

# Define a fixture to create a test user during testing
@pytest.fixture
def create_user():
    user_credential = client.post("/auth/signup", json={
        "email": "test@gmail.com", 'password': "12345678"
    })

# Define a fixture to authenticate a test user during testing
@pytest.fixture
def auth_user(create_user):
    user_credential = client.post("/auth/login", data={
        "username": "test@gmail.com",
        "password": "12345678",
    })
    # Return the user credentials in JSON format
    return user_credential.json()

# Define fixture to create a sample student for testing
@pytest.fixture
def create_sample_student():
    sample_student_data = {"name": "Test Student"}
    response = client.post("/students/", json=sample_student_data)
    return response.json()

# Define fixture to create sample attendance data for testing
@pytest.fixture
def create_sample_attendance():
    sample_attendance_data = {
        "student_id": "test_student_id",
        "session_id": "test_session_id",
        "present": True
    }
    response = client.post("/attendances/", json=sample_attendance_data)
    return response.json()

# Define fixture to create a sample user session for testing
@pytest.fixture
def create_sample_session(auth_user):
    sample_session_data = {"name": "Test Session"}
    response = client.post("/sessions/", json=sample_session_data, headers={
        "Authorization": f"Bearer {auth_user['access_token']}",
    })
    return response.json()