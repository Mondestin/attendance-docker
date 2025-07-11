from fastapi.testclient import TestClient
from main import app
from database.firebase import db
import pytest

# Create a TestClient instance for making HTTP requests
client = TestClient(app)


# Test case to get all attendance data
def test_get_attendance_data():
    response = client.get("/attendances/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Test case to create a new attendance record
def test_create_attendance():
    new_attendance_data = {
        "student_id": "test_student_id",
        "session_id": "test_session_id",
        "present": True
    }
    response = client.post("/attendances/", json=new_attendance_data)
    assert response.status_code == 201
    assert response.json()["student_id"] == "test_student_id"

# Test case to get an attendance record by ID
def test_get_attendance_by_id(create_sample_attendance):
    attendance_id = create_sample_attendance["id"]
    response = client.get(f"/attendances/{attendance_id}")
    assert response.status_code == 200
    assert response.json()["id"] == attendance_id

# Test case to modify an existing attendance record
def test_modify_attendance(create_sample_attendance):
    attendance_id = create_sample_attendance["id"]
    updated_data = {
        "student_id": "test_student_id",
        "session_id": "test_session_id",
        "present": False
    }
    response = client.patch(f"/attendances/{attendance_id}", json=updated_data)
    assert response.status_code == 200
    assert response.json()["present"] == False

# Test case to delete an attendance record
def test_delete_attendance(create_sample_attendance):
    attendance_id = create_sample_attendance["id"]
    response = client.delete(f"/attendances/{attendance_id}")
    assert response.status_code == 204
    assert db.child("attendances").child(attendance_id).get().val() is None
