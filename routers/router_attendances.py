import uuid
from fastapi import APIRouter, HTTPException
from database.firebase import db
from typing import List
from classes.schema_dto import Attendance, AttendanceNoID

router = APIRouter(
    tags=["Attendances"],
    prefix='/attendances'
)

@router.get('/', response_model=List[Attendance])
async def get_attendance_data():
    # Query attendance data from Firebase
    attendance_data = db.child('attendances').get().val()
    if attendance_data is not None:
        # Convert the dictionary of attendance data into a list of Attendance objects
        attendance_list = [Attendance(**data) for data in attendance_data.values()]
        return attendance_list
    else:
        # Return an empty list if no attendance data is found
        return []

@router.post('/', response_model=Attendance, status_code=201)
async def create_attendance(attendance_data: AttendanceNoID):
    # Generate a unique identifier for the new attendance record
    new_attendance_id = str(uuid.uuid4())
    # Create the new attendance record
    new_attendance = {
        'id': new_attendance_id,
        'student_id': attendance_data.student_id,
        'session_id': attendance_data.session_id,
        'present': attendance_data.present
    }
    # Store the new attendance record in Firebase
    db.child("attendances").child(new_attendance_id).set(new_attendance)
    # Return the newly created attendance record as a response
    return Attendance(**new_attendance)


@router.get('/{attendance_id}', response_model=Attendance)
async def get_attendance_by_ID(attendance_id:str): 
    # Query the attendance record by ID from Firebase
    attendance_data = db.child('attendances').child(attendance_id).get().val()
    if attendance_data is not None:
        # Return the attendance record
        return Attendance(**attendance_data)
    else:
        raise HTTPException(status_code=404, detail="Attendance record not found")


@router.patch('/{attendance_id}', response_model=Attendance)
async def modify_attendance(attendance_id: str, updated_data: AttendanceNoID):
    # Check if the attendance record exists
    existing_data = db.child('attendances').child(attendance_id).get().val()

    if existing_data is not None:
        # Update the attendance record with the provided data
        updated_data_dict = updated_data.dict(exclude_unset=True)
        db.child('attendances').child(attendance_id).update(updated_data_dict)
        updated_attendance_data = {**existing_data, **updated_data_dict}
        
        # Return the updated attendance record
        return Attendance(**updated_attendance_data)
    else:
        raise HTTPException(status_code=404, detail="Attendance record not found")



@router.delete('/{attendance_id}', status_code=204)
async def delete_attendance(attendance_id: str):
    # Check if the attendance record exists
    existing_data = db.child('attendances').child(attendance_id).get().val()

    if existing_data is not None:
        # Delete the attendance record from Firebase
        db.child('attendances').child(attendance_id).remove()
    else:
        raise HTTPException(status_code=404, detail="Attendance record not found")