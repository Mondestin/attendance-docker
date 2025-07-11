from fastapi import APIRouter, HTTPException
from typing import List
import uuid
from classes.schema_dto import Student, StudentNoID
from database.firebase import db

router= APIRouter(
    prefix='/students',
    tags=["Students"]
)

# Endpoints
@router.get('/', response_model=List[Student])
async def get_student():
     # Query all students' data from Firebase
    students_data = db.child('students').get().val()

    if students_data is not None:
        # Convert the dictionary of student data into a list of Student objects
        student_list = [Student(**data) for data in students_data.values()]
        # Return the list of student data
        return student_list
    else:
        # Return an empty list if no student data is found
        return []

# create new students 
@router.post('/', response_model=Student, status_code=201)
async def create_student(givenName:StudentNoID):
    # generate unique id
    generatedId=uuid.uuid4()
    # creation of student object
    newStudent= Student(id=str(generatedId), name=givenName.name)
     # Save the new Student in Firebase
    db.child('students').child(generatedId).set(newStudent.dict())
    # Return the created Student
    return newStudent


@router.get('/{student_id}', response_model=Student)
async def get_student_by_ID(student_id:str):
     # Query the student by ID from Firebase
    student_data = db.child('students').child(student_id).get().val()
    if student_data is not None:
        return Student(**student_data)
    else:
        raise HTTPException(status_code=404, detail="Student not found")


@router.patch('/{student_id}', status_code=204)
async def modify_student_name(student_id:str, modifiedStudent: StudentNoID):
    # Query the student by ID from Firebase
    student_data = db.child('students').child(student_id).get().val()

    if student_data is not None:
        # Update the student's data with the provided fields
        updated_fields = modifiedStudent.dict(exclude_unset=True)
        db.child('students').child(student_id).update(updated_fields)

        # Return the updated student data
        updated_student_data = {**student_data, **updated_fields}
        return Student(**updated_student_data)
    else:
        raise HTTPException(status_code=404, detail="Student not found")


@router.delete('/{student_id}', status_code=204)
async def delete_student(student_id:str):
    # Query the student by ID from Firebase
    student_data = db.child('students').child(student_id).get().val()

    if student_data is not None:
        # Delete the student's data
         db.child('students').child(student_id).remove()
    else:
        raise HTTPException(status_code=404, detail="Student not found")