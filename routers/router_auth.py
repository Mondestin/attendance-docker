from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from classes.schema_dto import User
from firebase_admin import auth
from database.firebase import authSession
from database.firebase import db
from fastapi.responses import RedirectResponse

router = APIRouter(
      tags=["Auth"],
      prefix='/auth'
)


#create new user
@router.post('/signup', status_code=201)
async def create_an_account(user_body: User):
    try:
        user = auth.create_user(
            email = user_body.email,
            password = user_body.password,
        )
        # stripe checkout url
        stripe_url = "http://localhost:8000/stripe/checkout"
        # redirect to stripe for subscription
        # return RedirectResponse(url=str(stripe_url))
        return {
        "message": f"User successfully create with id : {user.uid}"
        }
    
    except auth.EmailAlreadyExistsError:
        raise HTTPException(
            status_code=409,
            detail=f"Account already exist for : {user_body.email}"
        )

#Login endpoint 
@router.post('/login')
async def create_swagger_token(user_credentials:OAuth2PasswordRequestForm = Depends()):
    try:
        print(user_credentials)
        user = authSession.sign_in_with_email_and_password(
             email=user_credentials.username, 
             password = user_credentials.password)
        token = user['idToken']
        print(token)
        return {
            "access_token" : token,
            "token_type": "bearer"
        }
    except:
        raise HTTPException(
            status_code=401, details="Invalid Credentials"
        )
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# get current user token and verify
def get_current_user(provided_token: str = Depends(oauth2_scheme)):
    decoded_token = auth.verify_id_token(provided_token)
    decoded_token['idToken']=provided_token 
    return decoded_token

#Protect route to get personal data
@router.get('/me')
def secure_endoint(userData: int = Depends(get_current_user)):
    return userData
