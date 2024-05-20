import os
from models import *
from fastapi import APIRouter, HTTPException
from fastapi import Depends, status
from models import UserDefault, UserSubmodels, User, ChangePassword
from db.connection import get_session
from sqlalchemy import select
import datetime
from fastapi import Security, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from jose import jwt
from sqlmodel import select
import dotenv
dotenv.load_dotenv()

security = HTTPBearer()
pwd_context = CryptContext(schemes=['bcrypt'])
secret = os.environ.get("SECRET")
algorythm = os.environ.get("ALGORYTHM")


user_router = APIRouter()


@user_router.get("/users-list")
def users_list(session=Depends(get_session)) -> list[User]:
    return session.query(User).all()


def get_password_hash(password):
    return pwd_context.hash(password)


@user_router.post('/registration', status_code=201)
def register(user: UserDefault, session=Depends(get_session)):
    users = session.exec(select(User)).all()
    if any(x.username == user.username for x in users):
        raise HTTPException(status_code=400, detail='Username is taken')
    hashed_pwd = get_password_hash(user.password)
    user = User(username=user.username, password=hashed_pwd)
    session.add(user)
    session.commit()
    return {"status": 201, "message": "Created"}


def verify_password(pwd, hashed_pwd):
    return pwd_context.verify(pwd, hashed_pwd)


def encode_token(user_id):
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=8),
        'iat': datetime.datetime.utcnow(),
        'sub': user_id
    }
    return jwt.encode(payload, secret, algorithm=algorythm)


@user_router.post('/login')
def login(user: UserDefault, session=Depends(get_session)):
    user_found = session.exec(select(User).where(User.username == user.username)).first()
    if not user_found:
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    verified = verify_password(user.password, user_found.password)
    if not verified:
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    token = encode_token(user_found.username)
    return {'token': token}


def decode_token(token):
    try:
        payload = jwt.decode(token, secret, algorithms=[algorythm])
        return payload['sub']
    except Exception:
        raise HTTPException(status_code=401, detail='Token error')


def get_current_user(auth: HTTPAuthorizationCredentials = Security(security), session=Depends(get_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials'
    )
    username = decode_token(auth.credentials)
    if username is None:
        raise credentials_exception
    user = session.exec(select(User).where(User.username == username)).first()
    if user is None:
        raise credentials_exception
    return user


@user_router.get('/users/me')
def user_me(user: User = Depends(get_current_user)) -> UserSubmodels:
    return user


@user_router.patch("/users/me/reset-password")
def user_pwd(user_pwd: ChangePassword, session=Depends(get_session), current=Depends(get_current_user)):
    found_user = session.get(User, current.id)
    if not found_user:
        raise HTTPException(status_code=404, detail="User not found")
    verified = verify_password(user_pwd.old_password, found_user.password)
    if not verified:
        raise HTTPException(status_code=400, detail="Invalid old password")
    hashed_pwd = get_password_hash(user_pwd.new_password)
    found_user.password = hashed_pwd
    session.add(found_user)
    session.commit()
    session.refresh(found_user)
    return {"status": 200, "message": "password changed successfully"}
