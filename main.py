from fastapi import FastAPI
import db, auth

app = FastAPI()


@app.get("/login/")
async def login():
    pass