import datetime
from pydantic import BaseModel

# Model Pydantic = Datatype
class Student(BaseModel):
    id: str
    name: str

class Session(BaseModel):
    id: str
    name: str

# Attendance requests 
class Attendance(BaseModel):
    id:str
    student_id:str
    session_id:str
    present: bool


# No ID for Attendance requests   
class AttendanceNoID(BaseModel):
    student_id:str
    session_id:str
    present: bool

# No ID for Session requests 
class SessionNoID(BaseModel):
    name: str    

# No ID for Student requests 
class StudentNoID(BaseModel):
    name: str

# No ID for User requests 
class User(BaseModel):
    email: str
    password: str  
   
    