from fastapi import FastAPI, Depends,  HTTPException
from connection import init_db, get_session
from sqlalchemy import select
from typing_extensions import TypedDict
from models import *

app = FastAPI()


def on_startup():
    init_db()


app.add_event_handler("startup", on_startup)


@app.post("/case-create")
def case_create(case: CaseDefault, session=Depends(get_session)) \
        -> TypedDict('Response', {"status": int,
                                  "data": Case}):
    case = Case.model_validate(case)
    session.add(case)
    session.commit()
    session.refresh(case)
    return {"status": 200, "data": case}


@app.get("/cases-list")
def cases_list(session=Depends(get_session)) -> List[Case]:
    return session.query(Case).all()


@app.get("/case/{case_id}",  response_model=CaseSubmodels)
def case_get(case_id: int, session=Depends(get_session)):
    obj = session.get(Case, case_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="subcase not found")
    return obj


@app.patch("/case{case_id}")
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


@app.delete("/case/delete{case_id}")
def case_delete(case_id: int, session=Depends(get_session)):
    case = session.get(Case, case_id)
    if not case:
        raise HTTPException(status_code=404, detail="case not found")
    session.delete(case)
    session.commit()
    return {"ok": True}


@app.post("/subcase-create")
def subcase_create(subcase: SubcaseDefault, session=Depends(get_session)) \
        -> TypedDict('Response', {"status": int,
                                  "data": Subcase}):
    subcase = Subcase.model_validate(subcase)
    session.add(subcase)
    session.commit()
    session.refresh(subcase)
    return {"status": 200, "data": subcase}


@app.get("/subcases-list/{case_id}")
def subcases_list(case_id: int, session=Depends(get_session)) -> List[Subcase]:
    return session.query(Subcase).filter(Subcase.case_id == case_id).all()


@app.get("/subcase/{subcase_id}",  response_model=SubcaseSubmodels)
def subcase_get(subcase_id: int, session=Depends(get_session)) -> Subcase:
    obj = session.get(Subcase,  subcase_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="subcase not found")
    return obj


@app.patch("/subcase{subcase_id}")
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


@app.delete("/subcase/delete{subcase_id}")
def subcase_delete(subcase_id: int, session=Depends(get_session)):
    subcase = session.get(Subcase, subcase_id)
    if not subcase:
        raise HTTPException(status_code=404, detail="subcase not found")
    session.delete(subcase)
    session.commit()
    return {"ok": True}


@app.post("/message-create")
def message_create(message: MessageDefault, session=Depends(get_session)) \
        -> TypedDict('Response', {"status": int,
                                  "data": Message}):
    message = Message.model_validate(message)
    session.add(message)
    session.commit()
    session.refresh(message)
    return {"status": 200, "data": message}


@app.get("/messages-list/{subcase_id}")
def messages_list(subcase_id: int, session=Depends(get_session)) -> List[Message]:
    return session.query(Message).filter(Message.subcase_id == subcase_id).all()


@app.get("/message/{message_id}",  response_model=MessagesSubmodels)
def message_get(message_id: int, session=Depends(get_session)) -> Message:
    obj = session.get(Message,  message_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="message not found")
    return obj


@app.patch("/message{message_id}")
def message_update(message_id: int, message: MessageDefault, session=Depends(get_session)) -> Message:
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


@app.delete("/message/delete{message_id}")
def message_delete(message_id: int, session=Depends(get_session)):
    message = session.get(Message, message_id)
    if not message:
        raise HTTPException(status_code=404, detail="message not found")
    session.delete(message)
    session.commit()
    return {"ok": True}


@app.post("/user-create")
def user_create(user: UserDefault, session=Depends(get_session)) \
        -> TypedDict('Response', {"status": int,
                                  "data": User}):

    user = User.model_validate(user)
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"status": 200, "data": user}


@app.get("/users-list")
def users_list(session=Depends(get_session)) -> List[User]:
    return session.query(User).all()


@app.get("/user/{user_id}",  response_model=UserSubmodels)
def user_get(user_id: int, session=Depends(get_session)):
    obj = session.get(User, user_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="subuser not found")
    return obj


@app.patch("/user{user_id}")
def user_update(user_id: int, user: UserDefault, session=Depends(get_session)) -> User:
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="user not found")
    user_data = user.model_dump(exclude_unset=True)
    for key, value in user_data.items():
        setattr(db_user, key, value)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@app.patch("/set-user{user_id}-to-case", response_model=UserSubmodels)
def user_case_update(user_id: int, case: ManyToManyUpdate, session=Depends(get_session)) -> User:
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="user not found")

    case_id = case.case_id
    db_case = session.get(Case, case_id)
    if not db_case:
        raise HTTPException(status_code=404, detail="case not found")

    l_d = len(session.query(User).all())
    doing = Doing(id=l_d+1, user_id=user_id, case_id=case_id)
    session.add(doing)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.delete("/user/delete{user_id}")
def user_delete(user_id: int, session=Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    session.delete(user)
    session.commit()
    return {"ok": True}
