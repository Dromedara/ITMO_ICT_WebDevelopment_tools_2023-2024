from fastapi import APIRouter, HTTPException
from fastapi import Depends, status
from models import SubcaseDefault, SubcaseSubmodels, Subcase
from db.connection import get_session

subcase_router = APIRouter()


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
