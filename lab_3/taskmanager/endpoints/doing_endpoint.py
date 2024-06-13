from fastapi import APIRouter, HTTPException
from fastapi import Depends, status
from models import User, Doing, Case, ManyToManyUpdate, DoingSubmodels
from db.connection import get_session
from sqlalchemy import select

doing_router = APIRouter()


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