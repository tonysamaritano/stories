from unittest import result
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

import database as db


stripe.api_key = "sk_test_51MDdH0DrFDmQr8e1pI97uj8lleQCqgPOLrk7EcoYBLi6O27M3mg5VpLaBJwfem67b1DGFjMRe9cCNPemwQJZ0Jwt00pEaGiAy7"
CLIENT_ID = "294622490933-iglmkvhlsk9dmucq0etdp0tnkeqfj54j.apps.googleusercontent.com"
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"


class Token(BaseModel):
    token: str


class User(BaseModel):
    email: str
    first_name: str
    last_name: str
    picture: str
    tokens: int

    class Config:
        orm_mode = True


class PetRequest(BaseModel):
    name: str
    breed: str
    gender: str
    photo: Optional[str]


class PetPatch(BaseModel):
    name: Optional[str]
    breed: Optional[str]
    gender: Optional[str]
    photo: Optional[str]


class Pet(PetRequest):
    id: int
    owner: User

    class Config:
        orm_mode = True


class StoryRequest(BaseModel):
    adj_0: str
    adj_1: str
    adj_2: str
    backstory: Optional[str] = None
    details: Optional[str] = None


class Story(StoryRequest):
    id: int
    pet: Pet
    owner: str

    class Config:
        orm_mode = True


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

    result = db.session.query(db.User).filter(
        db.User.email == str(user["email"])).first()

    assert result is not None

    return User.from_orm(result)


@app.post("/{pet_id}/story")
async def story(pet_id: int, story: StoryRequest, bearer: Optional[str] = Cookie(None)):
    user = jwt.decode(bearer, SECRET_KEY, algorithms=[ALGORITHM])

    user_result = db.session.query(db.User).filter(
        db.User.email == str(user["email"])).first()

    query = db.session.query(db.Pet).filter(db.Pet.owner_id == user_result.id)
    result = query.filter(db.Pet.id == pet_id).first()

    if result is None:
        raise HTTPException(status_code=400, detail="Pet doesn't exist!")

    db_story = db.StoryRequest(owner=user_result.email, pet_id=pet_id, **story.dict())
    db.session.add(db_story)
    db.session.commit()
    db.session.refresh(db_story)

    return Story.from_orm(db_story)


@app.get("/story_requests")
async def story_requests(bearer: Optional[str] = Cookie(None)):
    user = jwt.decode(bearer, SECRET_KEY, algorithms=[ALGORITHM])

    result = db.session.query(db.StoryRequest).filter(
        db.StoryRequest.owner == user["email"]).all()

    if result is None:
        raise HTTPException(status_code=404, detail="No Story Requests")

    return [Story.from_orm(story) for story in result]


@app.post("/pet")
async def pet(pet: PetRequest, bearer: Optional[str] = Cookie(None)):
    user = jwt.decode(bearer, SECRET_KEY, algorithms=[ALGORITHM])

    user_result = db.session.query(db.User).filter(
        db.User.email == str(user["email"])).first()

    query = db.session.query(db.Pet).filter(db.Pet.owner_id == user_result.id)
    result = query.filter(db.Pet.name == pet.name).first()

    if result is not None:
        raise HTTPException(status_code=400, detail="Pet already exists")

    db_pet = db.Pet(owner_id=user_result.id, **pet.dict())
    db.session.add(db_pet)
    db.session.commit()
    db.session.refresh(db_pet)

    return Pet.from_orm(db_pet)


@app.get("/pet/{pet_id}")
async def pet(pet_id: int, bearer: Optional[str] = Cookie(None)):
    user = jwt.decode(bearer, SECRET_KEY, algorithms=[ALGORITHM])

    user_result = db.session.query(db.User).filter(
        db.User.email == str(user["email"])).first()

    query = db.session.query(db.Pet).filter(db.Pet.owner_id == user_result.id)
    result = query.filter(db.Pet.id == pet_id).first()

    if result is None:
        raise HTTPException(status_code=403, detail="Unauthorized")

    return Pet.from_orm(result)


@app.patch("/pet/{pet_id}")
async def pet(pet_id: int, pet: PetPatch, bearer: Optional[str] = Cookie(None)):
    user = jwt.decode(bearer, SECRET_KEY, algorithms=[ALGORITHM])

    user_result = db.session.query(db.User).filter(
        db.User.email == str(user["email"])).first()

    query = db.session.query(db.Pet).filter(db.Pet.owner_id == user_result.id)
    result = query.filter(db.Pet.id == pet_id).first()

    if result is None:
        raise HTTPException(status_code=400, detail="Pet doesn't exist!")

    pet_updated = {
        **Pet.from_orm(result).dict(),
        **pet.dict(exclude_none=True)
    }

    db_pet = db.Pet(**pet_updated)

    db.session.query(db.Pet).filter(
        db.Pet.id == pet_id).update(
            {db.Pet.photo: pet_updated["photo"], }
    )
    db.session.commit()

    # db.session.add(db_pet)
    # db.session.commit()

    # return Pet.from_orm(db_pet)

    return Pet(**pet_updated)


@app.get("/pets")
async def get_pet(bearer: Optional[str] = Cookie(None)):
    user = jwt.decode(bearer, SECRET_KEY, algorithms=[ALGORITHM])

    user_result = db.session.query(db.User).filter(
        db.User.email == str(user["email"])).first()

    query = db.session.query(db.Pet).filter(
        db.Pet.owner_id == user_result.id).all()

    return [Pet.from_orm(pet) for pet in query]


@app.post("/login")
async def login(token: Token):
    idinfo = id_token.verify_oauth2_token(
        token.token, requests.Request(), CLIENT_ID, clock_skew_in_seconds=60)

    result = db.session.query(db.User).filter(
        db.User.email == str(idinfo["email"])).first()

    # Creates a user if they don't exist
    if result is None:
        new_user = User(**dict({
            "email": idinfo["email"],
            "first_name": idinfo["given_name"],
            "last_name": idinfo["family_name"],
            "picture": idinfo["picture"],
            "tokens": 0,
        }))
        print(new_user)
        db_user = db.User(**new_user.dict())
        db.session.add(db_user)
        db.session.commit()

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

    result = db.session.query(db.User).filter(
        db.User.email == email).first()

    user = User.from_orm(result)

    line_items = stripe.checkout.Session.list_line_items(
        data["data"]["object"]["id"], limit=5)

    # print(line_items)

    qty = 0
    for item in line_items["data"]:
        if item["price"]["id"] == "price_1MDoNZDrFDmQr8e1JmVGqRvh":
            qty = 5
        elif item["price"]["id"] == "price_1MDfW4DrFDmQr8e1TOcYTc24":
            qty = 1

    print(f"{user.first_name} {user.last_name} <{user.email}> bought {qty} tokens")

    query = db.session.query(db.User).filter(db.User.email == email)
    query.update({db.User.tokens: user.tokens + qty})
    db.session.commit()

    return {"message": "Webhook!"}
