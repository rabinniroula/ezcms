from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
import db, auth

app = FastAPI()


@app.post("/login/")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    token = auth.getToken(username=form_data.username, password=form_data.password)
    if token != False:
        return {'access_token': token, 'token_type': 'bearer'}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )