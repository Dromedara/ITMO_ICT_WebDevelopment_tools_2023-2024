from fastapi import APIRouter, HTTPException
from fastapi import Depends, status
from models import CaseDefault, CaseSubmodels, Case
from db.connection import get_session

case_router = APIRouter()


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


