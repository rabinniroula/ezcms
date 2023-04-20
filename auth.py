from datetime import datetime, timedelta
from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from db import runQuery
from dotenv import load_dotenv
import os

DEBUG: bool = True
debug = lambda msg: print(msg) if DEBUG else None

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated=["auto"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def getToken(username: str, password: str) -> any:
    authResult = authenticateUser(username, password)
    if not authResult:
        debug("Username or password is wrong!")
        return False
    accessToken = createAccessToken({"username": username})
    return accessToken

def authenticateUser(uname: str, pwd: str) -> bool:
    try:
        retrievedPwd = runQuery(f"SELECT password FROM `users` WHERE username='{uname}'")[0][0]     # Need to use a better method than fetchall here. fetchall returns a list
    except:
        return False
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

def verifyToken(token: Annotated[str, Depends(oauth2_scheme)]) -> any:
    timenow = int(datetime.utcnow().timestamp())
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
    except JWTError:
        debug("Token is wrong!")
        return False
    expiryTime = payload["expiresIn"]
    if expiryTime >= timenow:
        debug('Token is expired!')
        return False
    return payload