from fastapi.testclient import TestClient
from main import app
from database.firebase import db
from classes.schema_dto import Student, StudentNoID
import uuid
import pytest

# Create a TestClient instance for making HTTP requests
client = TestClient(app)

# Test case to get all students
def test_get_students():
    response = client.get("/students/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Test case to create a new student
def test_create_student():
    new_student_data = {"name": "New Student"}
    response = client.post("/students/", json=new_student_data)
    assert response.status_code == 201
    assert response.json()["name"] == "New Student"

# Test case to get a student by ID
def test_get_student_by_id(create_sample_student):
    student_id = create_sample_student["id"]
    response = client.get(f"/students/{student_id}")
    assert response.status_code == 200
    assert response.json()["id"] == student_id

# Test case to modify an existing student's name
def test_modify_student_name(create_sample_student):
    student_id = create_sample_student["id"]
    updated_data = {"name": "Updated Student"}
    response = client.patch(f"/students/{student_id}", json=updated_data)
    assert response.status_code == 204

# Test case to delete a student
def test_delete_student(create_sample_student):
    student_id = create_sample_student["id"]
    response = client.delete(f"/students/{student_id}")
    assert response.status_code == 204
    assert db.child("students").child(student_id).get().val() is None
