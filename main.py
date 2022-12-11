from fastapi import FastAPI, Cookie, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from google.oauth2 import id_token
from google.auth.transport import requests

from pydantic import BaseModel
from typing import Optional
import json

from jose import jwt

import stripe

stripe.api_key = "sk_test_51MDdH0DrFDmQr8e1pI97uj8lleQCqgPOLrk7EcoYBLi6O27M3mg5VpLaBJwfem67b1DGFjMRe9cCNPemwQJZ0Jwt00pEaGiAy7"
CLIENT_ID = "294622490933-iglmkvhlsk9dmucq0etdp0tnkeqfj54j.apps.googleusercontent.com"
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"


class Token(BaseModel):
    token: str


class StoryRequest(BaseModel):
    name: str
    breed: str
    gender: str
    adj_0: str
    adj_1: str
    adj_2: str
    backstory: Optional[str] = None
    details: Optional[str]


class User(BaseModel):
    email: str
    first_name: str
    last_name: str
    picture: str
    tokens: int


fake_users_db = {
    "tonysam1@gmail.com": 0
}

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


@app.get("/me")
async def me(bearer: Optional[str] = Cookie(None)):
    try:
        user = jwt.decode(bearer, SECRET_KEY, algorithms=[ALGORITHM])
    except:
        raise HTTPException(status_code=401, detail="Not Logged In")

    if user["email"] not in fake_users_db:
        fake_users_db[user["email"]] = 0

    return User(tokens=fake_users_db[user["email"]], **user)


@app.post("/story")
async def story(story: StoryRequest, bearer: Optional[str] = Cookie(None)):
    print(story)

    try:
        decoded = jwt.decode(bearer, SECRET_KEY, algorithms=[ALGORITHM])
    except:
        raise HTTPException(status_code=401, detail="Not Logged In")

    print(decoded)

    stored_story = dict()
    stored_story["story"] = story.dict()
    stored_story["email"] = decoded["email"]

    with open("stories.txt", "a") as f:
        json.dump(stored_story, f, indent=2)
        f.write("\n")

    return {"message": "Hello World"}


@app.post("/login")
async def login(token: Token):
    idinfo = id_token.verify_oauth2_token(
        token.token, requests.Request(), CLIENT_ID, clock_skew_in_seconds=60)

    print(idinfo)

    encoded_jwt = jwt.encode({
        "email": idinfo["email"],
        "first_name": idinfo["given_name"],
        "last_name": idinfo["family_name"],
        "picture": idinfo["picture"],
    }, SECRET_KEY, algorithm=ALGORITHM)

    response = JSONResponse(content={"email": idinfo["email"]})
    response.set_cookie(
        key="bearer",
        value=encoded_jwt,
        httponly=True,
        secure=True)

    return response


@app.post("/logout")
async def logout():
    response = JSONResponse(content={"logout": "success"})
    response.delete_cookie(
        key="bearer",
        httponly=True,
        secure=True)

    return response


@app.post("/webhook")
async def webhook(stripe_webhook: Request):
    data = await stripe_webhook.json()

    email: str = data["data"]["object"]["customer_email"]

    line_items = stripe.checkout.Session.list_line_items(
        data["data"]["object"]["id"], limit=5)

    print(line_items)

    qty = 0
    for item in line_items["data"]:
        if item["price"]["id"] == "price_1MDoNZDrFDmQr8e1JmVGqRvh":
            qty = 5
        elif item["price"]["id"] == "price_1MDfW4DrFDmQr8e1TOcYTc24":
            qty = 1

    print(f"{email} bought {qty} tokens")

    if email in fake_users_db:
        fake_users_db[email] += qty
    else:
        fake_users_db[email] = qty

    return {"message": "Webhook!"}
