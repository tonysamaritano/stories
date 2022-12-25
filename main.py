import os
from unittest import result
from fastapi import FastAPI, Cookie, HTTPException, Request, status, Security
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from fastapi.security.base import SecurityBase


from google.oauth2 import id_token
from google.auth.transport import requests

from pydantic import BaseModel
from typing import Optional
import json

from jose import jwt, JWTError

import stripe

import database as db

# Environment variables
stripe.api_key = os.environ.get("STRIPE_API_KEY")
superuser: str = os.environ.get("SUPERUSER_EMAIL")


class Token(BaseModel):
    token: str


class User(BaseModel):
    email: str
    first_name: str
    last_name: str
    picture: str
    tokens: Optional[int] = 0

    class Config:
        orm_mode = True


class UserPatch(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    picture: Optional[str]
    tokens: Optional[int]


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


class StoryRequestData(BaseModel):
    adj_0: str
    adj_1: str
    adj_2: str
    backstory: Optional[str] = None
    details: Optional[str] = None


class StoryRequest(StoryRequestData):
    id: int
    pet: Pet
    owner: str
    status: str

    class Config:
        orm_mode = True


class StoryRequestPatch(BaseModel):
    adj_0: Optional[str] = None
    adj_1: Optional[str] = None
    adj_2: Optional[str] = None
    backstory: Optional[str] = None
    details: Optional[str] = None
    status:  Optional[str] = None


class Story(BaseModel):
    id: int
    owner: str

    request: StoryRequest

    img: Optional[str]
    content: Optional[str]
    title: Optional[str]
    preview: Optional[str]

    meta: Optional[str]

    class Config:
        orm_mode = True


class StoryPatch(BaseModel):
    owner: Optional[str] = None
    title: Optional[str] = None
    content: Optional[str] = None
    img: Optional[str] = None
    preview: Optional[str] = None
    meta:  Optional[str] = None


class AdminLogin(BaseModel):
    email: str


async def get_current_user(bearer: Optional[str] = Cookie(None)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        user = User(**jwt.decode(bearer,
                    os.environ.get("JWT_SECRET_KEY"),
                    algorithms=[os.environ.get("JWT_ALGORITHM")]))

        if user.email is None:
            raise credentials_exception

        # TODO: Add scopes
        # Allow access to all scopes if the user is an admin
        # if "Admin" not in user.scopes:
        #     for scope in security_scopes.scopes:
        #         if scope not in user.scopes:
        #             raise credentials_exception

    except JWTError:
        raise credentials_exception

    return user

app = FastAPI()

origins = [
    "https://www.petlegendary.com",
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
async def me(user: User = Security(get_current_user)):
    result = db.session.query(db.User).filter(
        db.User.email == str(user.email)).first()

    assert result is not None

    print(f"{result.first_name} {result.last_name} <{result.email}> logged in")

    return User.from_orm(result)


@app.post("/{pet_id}/story")
async def story(
    pet_id: int,
    story: StoryRequestData,
    user: User = Security(get_current_user)
):
    user_result = db.session.query(db.User).filter(
        db.User.email == str(user.email)).first()

    query = db.session.query(db.Pet).filter(db.Pet.owner_id == user_result.id)
    result = query.filter(db.Pet.id == pet_id).first()

    if result is None:
        raise HTTPException(status_code=400, detail="Pet doesn't exist!")

    db_story_request = db.StoryRequest(
        owner=user_result.email, pet_id=pet_id, **story.dict())
    db.session.add(db_story_request)
    db.session.commit()
    db.session.refresh(db_story_request)

    db_story = db.Story(owner=user_result.email,
                        request_id=db_story_request.id)

    db.session.add(db_story)
    db.session.commit()

    return StoryRequest.from_orm(db_story_request)


@app.get("/story_requests")
async def story_requests(user: User = Security(get_current_user)):
    result = db.session.query(db.StoryRequest).filter(
        db.StoryRequest.owner == user.email).all()

    if result is None:
        raise HTTPException(status_code=404, detail="No Story Requests")

    return [StoryRequest.from_orm(story) for story in result]


@app.get("/stories")
async def story_requests(user: User = Security(get_current_user)):
    result = db.session.query(db.Story).filter(
        db.Story.owner == user.email).all()

    if result is None:
        raise HTTPException(status_code=404, detail="No Story Requests")

    return [Story.from_orm(story) for story in result]


@app.get("/stories/{story_id}")
async def story_request(story_id: int, user: User = Security(get_current_user)):
    result = db.session.query(db.Story).filter(db.Story.id == story_id).first()

    if result is None:
        raise HTTPException(status_code=404, detail="No Story")

    if result.meta:
        try:
            meta = json.loads(result.meta)

            if meta["public"] == True:
                return Story.from_orm(result)
        except:
            pass

    if result.owner != user.email:
        raise HTTPException(status_code=403, detail="Unauthorized")

    return Story.from_orm(result)


@app.delete("/story_requests/{story_id}")
async def story_requests(story_id: int, user: User = Security(get_current_user)):
    query = db.session.query(db.StoryRequest).filter(
        db.StoryRequest.owner == user.email)
    result = query.filter(db.StoryRequest.id == story_id).first()

    if result is None:
        raise HTTPException(status_code=403, detail="No Story Requests")

    result = query.filter(db.StoryRequest.id == story_id).delete()
    db.session.commit()

    return {"deleted": result}


@app.post("/story_requests/{story_id}/apply")
async def story_requests(story_id: int, user: User = Security(get_current_user)):
    user_result = db.session.query(db.User).filter(
        db.User.email == str(user.email)).first()

    user = User.from_orm(user_result)

    if user.tokens < 1:
        raise HTTPException(status_code=406, detail="Not enough tokens")

    query = db.session.query(db.StoryRequest).filter(
        db.StoryRequest.owner == user.email)
    result = query.filter(db.StoryRequest.id == story_id).first()

    if result is None:
        raise HTTPException(status_code=403, detail="No Story Requests")

    if result.status != "accepted":
        raise HTTPException(
            status_code=403, detail="Story Request already applied to")

    print(f"consuming token {user.tokens}")

    db.session.query(db.User).filter(
        db.User.email == user.email).update(
            {db.User.tokens: user.tokens - 1, }
    )
    db.session.commit()
    db.session.refresh(user_result)

    user = User.from_orm(user_result)

    print(f"consumed token {user.tokens}")

    db.session.query(db.StoryRequest).filter(
        db.StoryRequest.id == story_id).update(
            {db.StoryRequest.status: "in_progress"}
    )
    db.session.commit()
    db.session.refresh(result)

    return result


@app.post("/pet")
async def pet(pet: PetRequest, user: User = Security(get_current_user)):
    user_result = db.session.query(db.User).filter(
        db.User.email == str(user.email)).first()

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
async def pet(pet_id: int, user: User = Security(get_current_user)):
    user_result = db.session.query(db.User).filter(
        db.User.email == str(user.email)).first()

    query = db.session.query(db.Pet).filter(db.Pet.owner_id == user_result.id)
    result = query.filter(db.Pet.id == pet_id).first()

    if result is None:
        raise HTTPException(status_code=403, detail="Unauthorized")

    return Pet.from_orm(result)


@app.patch("/pet/{pet_id}")
async def pet(pet_id: int, pet: PetPatch, user: User = Security(get_current_user)):
    user_result = db.session.query(db.User).filter(
        db.User.email == str(user.email)).first()

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

    return Pet(**pet_updated)


@app.get("/pets")
async def get_pet(user: User = Security(get_current_user)):
    user_result = db.session.query(db.User).filter(
        db.User.email == str(user.email)).first()

    query = db.session.query(db.Pet).filter(
        db.Pet.owner_id == user_result.id).all()

    return [Pet.from_orm(pet) for pet in query] if len(query) > 0 else None


@app.post("/login")
async def login(token: Token):
    idinfo = id_token.verify_oauth2_token(
        token.token,
        requests.Request(),
        os.environ.get("GOOGLE_CLIENT_ID"),
        clock_skew_in_seconds=60
    )

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
    }, os.environ.get("JWT_SECRET_KEY"), algorithm=os.environ.get("JWT_ALGORITHM"))

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

    if data["type"] != "checkout.session.completed":
        return {"status": "success"}

    email: str = data["data"]["object"]["customer_email"]

    result = db.session.query(db.User).filter(
        db.User.email == email).first()

    user = User.from_orm(result)

    line_items = stripe.checkout.Session.list_line_items(
        data["data"]["object"]["id"], limit=5)

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


@app.post("/admin/login")
async def login(login: AdminLogin, user: User = Security(get_current_user)):
    if user.email != superuser:
        raise HTTPException(status_code=403, detail="Unauthorized")

    result = db.session.query(db.User).filter(
        db.User.email == login.email).first()

    encoded_jwt = jwt.encode({
        "email": result.email,
        "first_name": result.first_name,
        "last_name": result.last_name,
        "picture": result.picture,
    },
        os.environ.get("JWT_SECRET_KEY"),
        algorithm=os.environ.get("JWT_ALGORITHM"))

    response = JSONResponse(content={"email": result.email})
    response.set_cookie(
        key="bearer",
        value=encoded_jwt,
        httponly=True,
        secure=True)

    return response


@app.get("/admin/pets")
async def get_pets(user: User = Security(get_current_user)):
    if user.email != superuser:
        raise HTTPException(status_code=403, detail="Unauthorized")

    return db.session.query(db.Pet).all()


@app.get("/admin/users")
async def get_pets(user: User = Security(get_current_user)):
    if user.email != superuser:
        raise HTTPException(status_code=403, detail="Unauthorized")

    return db.session.query(db.User).all()


@app.get("/admin/story_requests")
async def get_pets(user: User = Security(get_current_user)):
    if user.email != superuser:
        raise HTTPException(status_code=403, detail="Unauthorized")

    return db.session.query(db.StoryRequest).all()


@app.get("/admin/stories")
async def get_stories(user: User = Security(get_current_user)):
    if user.email != superuser:
        raise HTTPException(status_code=403, detail="Unauthorized")

    result = db.session.query(db.Story).all()

    return [Story.from_orm(story) for story in result]


@app.get("/admin/story/{story_id}")
async def get_stories(story_id: int, user: User = Security(get_current_user)):
    if user.email != superuser:
        raise HTTPException(status_code=403, detail="Unauthorized")

    result = db.session.query(db.Story).filter(db.Story.id == story_id).first()

    return Story.from_orm(result)


@app.post("/admin/story/{story_request_id}")
async def get_stories(story_request_id: int, user: User = Security(get_current_user)):
    if user.email != superuser:
        raise HTTPException(status_code=403, detail="Unauthorized")

    result = db.session.query(db.StoryRequest).filter(
        db.StoryRequest.id == story_request_id).first()

    if result is None:
        raise HTTPException(
            status_code=400, detail="Story Request doesn't exist!")

    db_story = db.Story(
        owner=superuser, request_id=story_request_id)
    db.session.add(db_story)
    db.session.commit()
    db.session.refresh(db_story)

    return db_story


@app.patch("/admin/story_requests/{story_request_id}")
async def patch_story_request(story_request_id: int, story_request: StoryRequestPatch, user: User = Security(get_current_user)):
    if user.email != superuser:
        raise HTTPException(status_code=403, detail="Unauthorized")

    result = db.session.query(db.StoryRequest).filter(
        db.StoryRequest.id == story_request_id).first()

    if result is None:
        raise HTTPException(
            status_code=400, detail="Story Request doesn't exist!")

    updated = {
        **StoryRequest.from_orm(result).dict(),
        **story_request.dict(exclude_none=True)
    }

    query = db.session.query(db.StoryRequest).filter(
        db.StoryRequest.id == story_request_id)
    query.update({
        db.StoryRequest.adj_0: updated["adj_0"],
        db.StoryRequest.adj_1: updated["adj_1"],
        db.StoryRequest.adj_2: updated["adj_2"],
        db.StoryRequest.status: updated["status"]
    })
    db.session.commit()
    db.session.refresh(result)

    return result


@app.patch("/admin/user/{user_id}")
async def patch_user(user_id: int, user_patch: UserPatch, user: User = Security(get_current_user)):
    if user.email != superuser:
        raise HTTPException(status_code=403, detail="Unauthorized")

    result = db.session.query(db.User).filter(db.User.id == user_id).first()

    if result is None:
        raise HTTPException(
            status_code=400, detail="User doesn't exist!")

    updated = {
        **User.from_orm(result).dict(),
        **user_patch.dict(exclude_none=True)
    }

    query = db.session.query(db.User).filter(
        db.User.id == user_id)
    query.update({
        db.User.tokens: updated["tokens"],
    })
    db.session.commit()
    db.session.refresh(result)

    return result


@app.patch("/admin/pet/{pet_id}")
async def patch_pet(pet_id: int, pet_patch: PetPatch, user: User = Security(get_current_user)):
    if user.email != superuser:
        raise HTTPException(status_code=403, detail="Unauthorized")

    result = db.session.query(db.Pet).filter(db.Pet.id == pet_id).first()

    if result is None:
        raise HTTPException(
            status_code=400, detail="User doesn't exist!")

    updated = {
        **Pet.from_orm(result).dict(),
        **pet_patch.dict(exclude_none=True)
    }

    query = db.session.query(db.Pet).filter(
        db.Pet.id == pet_id)
    query.update({
        db.Pet.name: updated["name"],
        db.Pet.breed: updated["breed"],
        db.Pet.gender: updated["gender"],
        db.Pet.photo: updated["photo"],
    })
    db.session.commit()
    db.session.refresh(result)

    return result


@app.patch("/admin/story/{story_id}")
async def patch_story(story_id: int, story_patch: StoryPatch, user: User = Security(get_current_user)):
    if user.email != superuser:
        raise HTTPException(status_code=403, detail="Unauthorized")

    result = db.session.query(db.Story).filter(db.Story.id == story_id).first()

    if result is None:
        raise HTTPException(
            status_code=400, detail="User doesn't exist!")

    updated = {
        **Story.from_orm(result).dict(),
        **story_patch.dict(exclude_none=True)
    }

    query = db.session.query(db.Story).filter(
        db.Story.id == story_id)
    query.update({
        db.Story.owner: updated["owner"],
        db.Story.title: updated["title"],
        db.Story.content: updated["content"],
        db.Story.preview: updated["preview"],
        db.Story.img: updated["img"],
        db.Story.meta: updated["meta"],

    })
    db.session.commit()
    db.session.refresh(result)

    return result

@app.get("/admin/export")
async def patch_story(user: User = Security(get_current_user)):
    if user.email != superuser:
        raise HTTPException(status_code=403, detail="Unauthorized")

    users = db.session.query(db.User).all()
    requests = db.session.query(db.StoryRequest).all()
    pets = db.session.query(db.Pet).all()
    stories = db.session.query(db.Story).all()

    return {
        "users": users,
        "requests": requests,
        "pets": pets,
        "stories": stories
    }
