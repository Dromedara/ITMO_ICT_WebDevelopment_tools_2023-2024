from fastapi import FastAPI, BackgroundTasks
from parse import parse_and_save
from database import get_session
from fastapi import Depends, status
from models import Parce
app = FastAPI()


@app.post("/parse/")
async def parse(url: str, background_tasks: BackgroundTasks, session=Depends(get_session)):
    background_tasks.add_task(parse_and_save, url, session)
    return {"message": "Parse started."}


@app.get("/get-tasks/")
def cases_list(session=Depends(get_session)) -> list[Parce]:
    return session.query(Parce).all()