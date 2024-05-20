# Лабораторная 1

## Структура проекта

```plaintext
project/
│
├── db/
│   └── connection.py
│
├── endpoints/
│   ├── case_endpoints.py
│   ├── subcase_endpoint.py
│   ├── message_endpoint.py
│   ├── doing_endpoint.py
│   └── user_endpoints.py
│
└── main.py
```

## Маршруты API

### Cases

- **Префикс:** `/api/cases`
- **Тег:** `cases`
- **Маршрутизатор:** `case_router`

### Subcases

- **Префикс:** `/api/subcases`
- **Тег:** `subcases`
- **Маршрутизатор:** `subcase_router`

### Messages

- **Префикс:** `/api/messages`
- **Тег:** `messages`
- **Маршрутизатор:** `message_router`

### Doings

- **Префикс:** `/api/doing`
- **Тег:** `doings`
- **Маршрутизатор:** `doing_router`

### Users

- **Префикс:** `/api`
- **Тег:** `users`
- **Маршрутизатор:** `user_router`

## main.py

Основной файл приложения, который настраивает и запускает FastAPI приложение.

### Импорт необходимых модулей

```python
from fastapi import FastAPI
import uvicorn
from db.connection import init_db
from endpoints.case_endpoints import case_router
from endpoints.subcase_endpoint import subcase_router
from endpoints.message_endpoint import message_router
from endpoints.doing_endpoint import doing_router
from endpoints.user_endpoints import user_router
```

### Создание экземпляра приложения

```python
app = FastAPI()
```

### Подключение маршрутизаторов

```python

app.include_router(case_router, prefix="/api/cases", tags=["cases"])
app.include_router(subcase_router, prefix="/api/subcases", tags=["subcases"])
app.include_router(message_router, prefix="/api/messages", tags=["messages"])
app.include_router(doing_router, prefix="/api/doing", tags=["doings"])
app.include_router(user_router, prefix="/api", tags=["users"])
```


### Инициализация базы данных

```python

@app.on_event("startup")
def on_startup():
    init_db()
```


### Запуск приложения

```python

if __name__ == '__main__':
    uvicorn.run('main:app', host="localhost", port=8000, reload=True)
```


## connetion.py 

Файл, отвечающий за соединение с базой данных


### Подключение зависимостей
```python
from sqlmodel import SQLModel, Session, create_engine
import os
from dotenv import load_dotenv
```


### Подгрузка переменных среды и создание канала связи с БД 

```python
load_dotenv()
db_url = os.getenv('DB_ADMIN')
engine = create_engine(db_url, echo=True)
```

### Создание/обновление БД
```python
def init_db():
    SQLModel.metadata.create_all(engine)
```

### Создание сессии обмена данными
```python
def get_session():
    with Session(engine) as session:
        yield session
```

## models.py

Файл, отвечающий за конфигурацию базы данных.


### Импорт необходимых модулей

```python
import datetime
from pydantic import BaseModel
from enum import Enum
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
```

###  Message

```python
class ReadMessageUpdate(SQLModel):
    seemed: bool


class MessageDefault(SQLModel):
    message: str
    seemed: bool
    doing_id: Optional[int] = Field(default=None, foreign_key="doing.id")


class MessagesSubmodels(MessageDefault):
    doing: Optional["Doing"] = None


class Message(MessageDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    doing: Optional["Doing"] = Relationship(back_populates="messages")
```

###  Task 
```python
class DoingDefault(SQLModel):
    case_id: Optional[int] = Field(
        default=None, foreign_key="case.id"
    )
    user_id: Optional[int] = Field(
        default=None, foreign_key="user.id"
    )


class DoingSubmodels(DoingDefault):
    time_spent: datetime.timedelta = None
    cases: Optional["Case"] = None
    users: Optional["User"] = None
    messages: Optional[List["Message"]] = None


class Doing(DoingDefault,  table=True):
    id: int = Field(default=None, primary_key=True)
    time_spent: datetime.timedelta = datetime.timedelta(seconds=0)

    cases: Optional["Case"] = Relationship(back_populates="doings")
    users: Optional["User"] = Relationship(back_populates="doings")
    messages: Optional[List["Message"]] = Relationship(back_populates="doing",
                                                       sa_relationship_kwargs={
                                                           "cascade": "all, delete",
                                                       }
                                                       )

class ManyToManyUpdate(BaseModel):
    time_spent: datetime.timedelta = datetime.timedelta(seconds=0)

```

###  Subcase

```python Subcase
class SubcaseDefault (SQLModel):
    what_to_do: str
    comment: str
    deadline: datetime.datetime
    case_id: Optional[int] = Field(default=None, foreign_key="case.id")


class SubcaseSubmodels(SubcaseDefault):
    case: Optional["Case"] = None


class Subcase(SubcaseDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    case: Optional["Case"] = Relationship(back_populates="subcases")
```

###  Case  
```python

class Priority(Enum):
    super_high = "super_high"
    high = "high"
    normal = "normal"
    low = "low"
    super_low = "super_low"
    
class CaseDefault(SQLModel):
    name: str
    description: str
    priority: Priority


class CaseSubmodels(CaseDefault):
    subcases: Optional[List["Subcase"]] = None
    users: Optional[List["User"]] = None


class Case(CaseDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    subcases: Optional[List["Subcase"]] = Relationship(back_populates="case",
                                          sa_relationship_kwargs={
                                              "cascade": "all, delete",
                                          }
                                          )

    users: Optional[List["User"]] = Relationship(
        back_populates="cases", link_model=Doing
    )
    doings: Optional[List["Doing"]] = Relationship(back_populates="cases")
```

###  User  

```python
class UserDefault(SQLModel):
    username: str
    password: str


class UserSubmodels(UserDefault):
    cases: Optional[List["Case"]] = None
    doings: Optional[List["Doing"]] = None


class User(UserDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    cases: Optional[List["Case"]] = Relationship(
        back_populates="users", link_model=Doing
    )
    doings: Optional[List["Doing"]] = Relationship(back_populates="users")


class ChangePassword(SQLModel):
    old_password: str
    new_password: str
```

# CRUD

## Case endpoints

### Роутер кейсов

```python
case_router = APIRouter()
```

### Эндпоинты для создания, отображения, изменения и удаления объектов

```python
@case_router.post("/create", status_code=status.HTTP_201_CREATED)
def case_create(case: CaseDefault, session=Depends(get_session)) \
        -> Case:
    case = Case.model_validate(case)
    session.add(case)
    session.commit()
    session.refresh(case)
    return case


@case_router.get("/list", status_code=status.HTTP_200_OK)
def cases_list(session=Depends(get_session)) -> list[Case]:
    return session.query(Case).all()


@case_router.get("/{case_id}", status_code=status.HTTP_200_OK,  response_model=CaseSubmodels)
def case_get(case_id: int, session=Depends(get_session)) -> Case:
    obj = session.get(Case, case_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="subcase not found")
    return obj


@case_router.patch("/update-{case_id}", status_code=status.HTTP_202_ACCEPTED)
def case_update(case_id: int, case: CaseDefault, session=Depends(get_session)) -> Case:
    db_case = session.get(Case, case_id)
    if not db_case:
        raise HTTPException(status_code=404, detail="Case not found")
    case_data = case.model_dump(exclude_unset=True)
    for key, value in case_data.items():
        setattr(db_case, key, value)
    session.add(db_case)
    session.commit()
    session.refresh(db_case)
    return db_case


@case_router.delete("/delete{case_id}", status_code=status.HTTP_204_NO_CONTENT)
def case_delete(case_id: int, session=Depends(get_session)):
    case = session.get(Case, case_id)
    if not case:
        raise HTTPException(status_code=404, detail="case not found")
    session.delete(case)
    session.commit()
    return {"ok": True}
```

## Doing endpoints

### Роутер Выполнения вейсов

```python
doing_router = APIRouter()
```

### Эндпоинты для создания, отображения, изменения и удаления объектов

```python
@doing_router.post("/set-user{user_id}-to-case{case_id}", status_code=status.HTTP_201_CREATED)
def user_case_update(user_id: int, case_id: int, session=Depends(get_session)) ->\
        Doing:
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="user not found")

    db_case = session.get(Case, case_id)
    if not db_case:
        raise HTTPException(status_code=404, detail="case not found")

    doing = Doing(user_id=user_id, case_id=case_id)
    session.add(doing)
    session.commit()
    session.refresh(doing)

    return doing


@doing_router.get("/get-user{user_id}-to-case{case_id}", status_code=status.HTTP_200_OK, response_model=DoingSubmodels)
def user_case_get(user_id: int, case_id: int, session=Depends(get_session)) -> Doing:
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="user not found")

    db_case = session.get(Case, case_id)
    if not db_case:
        raise HTTPException(status_code=404, detail="case not found")

    qs = session.exec(select(Doing).where(Doing.case_id == case_id).where(Doing.user_id == user_id))
    doing = qs.first()

    if not doing:
        raise HTTPException(status_code=404, detail="User was not associated with this case.")

    return doing[0]


@doing_router.delete("/remove-user{user_id}-from-case{case_id}", status_code=status.HTTP_204_NO_CONTENT)
def user_case_delete(user_id: int, case_id: int, session=Depends(get_session)):
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="user not found")

    db_case = session.get(Case, case_id)
    if not db_case:
        raise HTTPException(status_code=404, detail="case not found")

    qs = session.exec(select(Doing).where(Doing.case_id == case_id).where(Doing.user_id == user_id))
    doing = qs.first()

    if not doing:
        raise HTTPException(status_code=404, detail="User was not associated with this case.")

    session.delete(doing[0])
    session.commit()
    return {"ok": True}


@doing_router.patch("/update-user{user_id}-from-case{case_id}", status_code=status.HTTP_202_ACCEPTED,
                    response_model=DoingSubmodels)
def user_case_update(user_id: int, case_id: int, doing_data: ManyToManyUpdate, session=Depends(get_session)) -> Doing:
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="user not found")
    db_case = session.get(Case, case_id)
    if not db_case:
        raise HTTPException(status_code=404, detail="case not found")

    qs = session.exec(select(Doing).where(Doing.case_id == case_id).where(Doing.user_id == user_id))
    doing = qs.first()
    if not doing:
        raise HTTPException(status_code=404, detail="User was not associated with this case.")

    db_doing = doing[0]
    doing_data = doing_data.model_dump(exclude_unset=True)
    for key, value in doing_data.items():
        setattr(db_doing, key, value)
    session.add(db_doing)
    session.commit()
    session.refresh(db_doing)
    return db_doing
```

## Subcase endpoints

### Роутер суб-кейсов

```python
subcase_router = APIRouter()
```

### Эндпоинты для создания, отображения, изменения и удаления объектов

```python
@subcase_router.post("/create", status_code=status.HTTP_201_CREATED)
def subcase_create(subcase: SubcaseDefault, session=Depends(get_session)) \
        -> Subcase:
    subcase = Subcase.model_validate(subcase)
    session.add(subcase)
    session.commit()
    session.refresh(subcase)
    return subcase


@subcase_router.get("/list-in/{case_id}", status_code=status.HTTP_200_OK)
def subcases_list(case_id: int, session=Depends(get_session)) -> list[Subcase]:
    return session.query(Subcase).filter(Subcase.case_id == case_id).all()


@subcase_router.get("/{subcase_id}", status_code=status.HTTP_200_OK,  response_model=SubcaseSubmodels)
def subcase_get(subcase_id: int, session=Depends(get_session)) -> Subcase:
    obj = session.get(Subcase,  subcase_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="subcase not found")
    return obj


@subcase_router.patch("/update-{subcase_id}", status_code=status.HTTP_202_ACCEPTED)
def subcase_update(subcase_id: int, subcase: SubcaseDefault, session=Depends(get_session)) -> Subcase:
    db_subcase = session.get(Subcase, subcase_id)
    if not db_subcase:
        raise HTTPException(status_code=404, detail="subcase not found")
    subcase_data = subcase.model_dump(exclude_unset=True)
    for key, value in subcase_data.items():
        setattr(db_subcase, key, value)
    session.add(db_subcase)
    session.commit()
    session.refresh(db_subcase)
    return db_subcase


@subcase_router.delete("/delete{subcase_id}", status_code=status.HTTP_204_NO_CONTENT)
def subcase_delete(subcase_id: int, session=Depends(get_session)):
    subcase = session.get(Subcase, subcase_id)
    if not subcase:
        raise HTTPException(status_code=404, detail="subcase not found")
    session.delete(subcase)
    session.commit()
    return {"ok": True}

```

## Message endpoints

### Роутер сообщений

```python
message_router = APIRouter()
```

### Эндпоинты для создания, отображения, изменения и удаления объектов

```python
@message_router.post("/create", status_code=status.HTTP_201_CREATED)
def message_create(message: MessageDefault, session=Depends(get_session)) \
        -> Message:
    message = Message.model_validate(message)
    session.add(message)
    session.commit()
    session.refresh(message)
    return message


@message_router.get("/list-in/{doing_id}", status_code=status.HTTP_200_OK)
def messages_list(doing_id: int, session=Depends(get_session)) -> list[Message]:
    return session.query(Message).filter(Message.doing_id == doing_id).all()


@message_router.get("/{message_id}", status_code=status.HTTP_200_OK,  response_model=MessagesSubmodels)
def message_get(message_id: int, session=Depends(get_session)) -> Message:
    obj = session.get(Message,  message_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="message not found")
    return obj


@message_router.patch("/update-{message_id}", status_code=status.HTTP_202_ACCEPTED)
def message_update(message_id: int, message: ReadMessageUpdate, session=Depends(get_session)) -> Message:
    db_message = session.get(Message, message_id)
    if not db_message:
        raise HTTPException(status_code=404, detail="message not found")
    message_data = message.model_dump(exclude_unset=True)
    for key, value in message_data.items():
        setattr(db_message, key, value)
    session.add(db_message)
    session.commit()
    session.refresh(db_message)
    return db_message


@message_router.delete("/delete{message_id}", status_code=status.HTTP_204_NO_CONTENT)
def message_delete(message_id: int, session=Depends(get_session)):
    message = session.get(Message, message_id)
    if not message:
        raise HTTPException(status_code=404, detail="message not found")
    session.delete(message)
    session.commit()
    return {"ok": True}
```

## User endpoints

### Подгрузка переменных среды, создание глобальных переменных, роутера пользователей

```python
dotenv.load_dotenv()
security = HTTPBearer()
pwd_context = CryptContext(schemes=['bcrypt'])
secret = os.environ.get("SECRET")
algorythm = os.environ.get("ALGORYTHM")
user_router = APIRouter()

```

### Эндпоинты для создания, отображения, изменения и удаления объектов

А так же функции для ахэширования пароля, кодирования и декодирования токена, авторизация пользователя

```python

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
```