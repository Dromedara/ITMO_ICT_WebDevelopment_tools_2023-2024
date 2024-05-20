import datetime
from pydantic import BaseModel
from enum import Enum
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class Priority(Enum):
    super_high = "super_high"
    high = "high"
    normal = "normal"
    low = "low"
    super_low = "super_low"


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


class ManyToManyUpdate(BaseModel):
    time_spent: datetime.timedelta = datetime.timedelta(seconds=0)

