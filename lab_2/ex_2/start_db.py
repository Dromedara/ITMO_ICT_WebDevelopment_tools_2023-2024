from sqlmodel import SQLModel, create_engine, Session
import os
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv("DB_URL")

engine = create_engine(db_url, echo=True)


def create_database_session() -> Session:
    return Session(bind=engine)


def init_db() -> None:
    SQLModel.metadata.create_all(engine)

from sqlmodel import Field, SQLModel


class Parce(SQLModel, table=True):
    id: int = Field(primary_key=True)
    url: str
    title: str
    process_type: str


init_db()