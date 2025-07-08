#from typing import List, Union
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from datetime import datetime, timedelta
from sqlmodel import Session, select
from database import create_db_and_tables, get_session
from model import User, Token, TokenData

app = FastAPI()

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

#setup db tables
@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    
def createAccessToken(username):
    data = {"sub": username}
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def passwordVerify(userPassword, dbPassword):
    return pwd_context.verify(userPassword, dbPassword)

def loginUser(username : str, password : str, db):
    user = db.exec(select(User).where(User.username == username)).first()
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password"
        )
    if not passwordVerify(password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password"
        )
    return user

def getCurrentUser(token : str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    return data
        

#rest of the code: endpoints etc.
@app.post('/login', status_code=200)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)):
    user = loginUser(form_data.username, form_data.password, db)
    access_token = createAccessToken(user.username)
    return Token(access_token=access_token, token_type="bearer")
    
@app.get('/logged', status_code=200)
async def getLoggedUser(user = Depends(getCurrentUser)):
    return user

@app.get('/hello', status_code=200)
async def hello():
    return "hello"
        
        
