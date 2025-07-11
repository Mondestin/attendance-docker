from fastapi.testclient import TestClient
from main import app
from database.firebase import db
from classes.schema_dto import Session, SessionNoID
from routers.router_auth import get_current_user
import uuid
import pytest

# Create a TestClient instance for making HTTP requests
client = TestClient(app)

# Test case to get all user sessions
def test_get_sessions(auth_user, create_sample_session):
    response = client.get("/sessions/", headers={
        "Authorization": f"Bearer {auth_user['access_token']}",
    })
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Test case to create a new user session
def test_create_session(auth_user):
    new_session_data = {"name": "New Session"}
    response = client.post("/sessions/", json=new_session_data, headers={
        "Authorization": f"Bearer {auth_user['access_token']}",
    })
    assert response.status_code == 201
    assert response.json()["name"] == "New Session"

# Test case to modify an existing user session's name
def test_modify_session_name(auth_user, create_sample_session):
    session_id = create_sample_session["id"]
    updated_data = {"name": "Updated Session"}
    response = client.patch(f"/sessions/{session_id}", json=updated_data, headers={
        "Authorization": f"Bearer {auth_user['access_token']}",
    })
    assert response.status_code == 204

# Test case to delete a user session
def test_delete_session(auth_user, create_sample_session):
    session_id = create_sample_session["id"]
    response = client.delete(f"/sessions/{session_id}", headers={
        "Authorization": f"Bearer {auth_user['access_token']}",
    })
    assert response.status_code == 204
    
