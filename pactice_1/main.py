from fastapi import FastAPI
from DBsaver import project_db
from typing import Optional, List
from typing_extensions import TypedDict
from models import *

app = FastAPI()


#################### USER

@app.get("/users_list")
def users_list() -> List[User]:
    return project_db


@app.get("/user/{user_id}")
def user_get(user_id: int) -> User|str:
    user = None
    for user in project_db:
        if user.get("id") == user_id:
            user = user
    if user:
        return user
    else:
        return "ERROR_400: User with such id was not found"


@app.post("/user")
def users_create(user: User) -> TypedDict('Response', {"status": int, "data": User}):
    user_to_append = user.model_dump()
    project_db.append(user_to_append)
    return {"status": 200, "data": user}


@app.delete("/user/delete{user_id}")
def user_delete(user_id: int):
    for i, user in enumerate(project_db):
        if user.get("id") == user_id:
            project_db.pop(i)
            break
    return {"status": 201, "message": "deleted"}


@app.put("/user{user_id}")
def user_update(user_id: int, user: User) -> List[User]:
    for user_data in project_db:
        if user_data.get("id") == user_id:
            user_to_append = user.model_dump()
            project_db.remove(user_data)
            project_db.append(user_to_append)
    return project_db

#################### CASE


@app.get("/cases_list")
def cases_list() -> List[Case]:
    cases_responce = []
    for user in project_db:
        doing_objs = user.get("doing")
        for obj in doing_objs:
            case = obj.get("case")
            cases_responce.append(case)
    return cases_responce


@app.get("/case/{case_id}")
def case_get(case_id: int) -> Case | str:
    case_to_find = None
    for user in project_db:
        doing_objs = user.get("doing")
        for obj in doing_objs:
            case = obj.get("case")
            if case.get("id") == case_id:
                case_to_find = case

    if case_to_find:
        return case_to_find
    else:
        return "ERROR_400: case with such id was not found"


@app.post("/case")
def cases_create(user_id: int, doing_id: int, case: Case) -> TypedDict('Response', {"status": int, "data": Case}):
    case_to_append = case.model_dump()
    for user in project_db:
        if user.get("id") == user_id:
            doing = user.get("doing")
            doing_data = {
                "id": doing_id,
                "time_spent": 0
            }
            doing_data["case"] = case_to_append
            doing.append(doing_data)
    return {"status": 200, "data": case}


@app.delete("/case/delete{case_id}")
def case_delete(case_id: int):
    for user in project_db:
        doing_objs = user.get("doing")
        for i, obj in enumerate(doing_objs):
            case = obj.get("case")
            if case.get("id") == case_id:
                obj.pop(i)
                break
    return {"status": 201, "message": "deleted"}


@app.put("/case{case_id}")
def case_update(case_id: int, case: Case) -> Case:
    for user in project_db:
        doing_objs = user.get("doing")
        for obj in doing_objs:
            case_data = obj.get("case")
            if case_data.get("id") == case_id:
                case_to_append = case.model_dump()
                obj["case"] = case_to_append
    return case_to_append