from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from google.oauth2 import id_token
from google.auth.transport import requests

from pydantic import BaseModel

CLIENT_ID = "294622490933-iglmkvhlsk9dmucq0etdp0tnkeqfj54j.apps.googleusercontent.com"


class Token(BaseModel):
    token: str


app = FastAPI()

origins = [
    "https://dev.tonysamaritano.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/login")
async def login(token: Token):

    print(token.token)
    idinfo = id_token.verify_oauth2_token(
        token.token, requests.Request(), CLIENT_ID)

    return idinfo
