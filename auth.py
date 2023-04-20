from datetime import datetime, timedelta
from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from db import runQuery
from dotenv import load_dotenv
import os

load_dotenv()

class password_wrong_exception(BaseException):
    def __init__(self) -> None:
        super().__init__("Password is wrong!")

class token_wrong_exception(BaseException):
    def __init__(self) -> None:
        super().__init__("Token is wrong!")

class token_expired_exception(BaseException):
    def __init__(self) -> None:
        super().__init__("Token is expired! Login again!")
        

pwd_context = CryptContext(schemes=["bcrypt"], deprecated=["auto"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def getToken(username: str, password: str) -> any:
    user = authenticateUser(username, password)
    if not user:
        raise password_wrong_exception
    accessToken = createAccessToken({"username": username})
    return accessToken

def authenticateUser(uname: str, pwd: str) -> bool:
    try:
        retrievedPwd = runQuery(f"SELECT password FROM `users` WHERE username='{uname}'")[0][0]
    except:
        raise password_wrong_exception
    if pwd_context.verify(pwd, retrievedPwd):
        return True
    else:
        return False

def createAccessToken(data: dict) -> str:
    toEncode = data
    expiresIn = int((datetime.utcnow() + timedelta(hours=5)).timestamp())
    toEncode.update({"expiresIn": expiresIn})
    encoded = jwt.encode(toEncode, key = os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))
    return encoded

def verifyToken(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
    timenow = int(datetime.utcnow().timestamp())
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
    except JWTError:
        raise token_wrong_exception
    expiryTime = payload["expiresIn"]
    if expiryTime >= timenow:
        raise token_expired_exception
    return payload