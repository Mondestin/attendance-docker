from fastapi import APIRouter, Depends, HTTPException
from typing import List
import uuid
from classes.schema_dto import Session, SessionNoID
from database.firebase import db
from routers.router_auth import get_current_user
from routers.router_stripe import increment_stripe

router= APIRouter(
    prefix='/sessions',
    tags=["Sessions"]
)
# get all users sessions
@router.get('/', response_model=List[Session])
async def get_sessions(userData: int = Depends(get_current_user)):
    # List all the Sessions from a Training Center
    fireBaseobject = db.child("users").child(userData['uid']).child('sessions').get(userData['idToken']).val()
    resultArray = [value for value in fireBaseobject.values()]
    return resultArray

# create new user session name
@router.post('/', response_model=Session, status_code=201)
async def create_sessions(givenName:SessionNoID, userData: int = Depends(get_current_user)):
    generatedId=uuid.uuid4()
    newSession= Session(id=str(generatedId), name=givenName.name)
    print("the current user uid is:" + userData['uid'])
    # increment_stripe(userData['uid'])
    db.child("users").child(userData['uid']).child("sessions").child(str(generatedId)).set(newSession.dict(), userData['idToken'])
    return newSession

# update user's session name
@router.patch('/{session_id}', status_code=204)
async def modify_student_name(session_id:str, modifiedSession: SessionNoID, userData: int = Depends(get_current_user)):
    fireBaseobject = db.child("users").child(userData['uid']).child('sessions').child(session_id).get(userData['idToken']).val()
    if fireBaseobject is not None:
        updatedSession = Session(id=session_id, **modifiedSession.dict())
        return db.child("users").child(userData['uid']).child('sessions').child(session_id).update(updatedSession.dict(), userData['idToken'] )
    raise HTTPException(status_code= 404, detail="Session not found")

# delete a session from user's sessions
@router.delete('/{session_id}', status_code=204)
async def delete_session(session_id:str, userData: int = Depends(get_current_user)):
    try:
        fireBaseobject = db.child("users").child(userData['uid']).child('sessions').child(session_id).get(userData['idToken']).val()
    except:
        raise HTTPException(
            status_code=403, detail="Accès interdit"
        )
    if fireBaseobject is not None:
        return db.child("users").child(userData['uid']).child('sessions').child(session_id).remove(userData['idToken'])
    raise HTTPException(status_code= 404, detail="Session not found")
