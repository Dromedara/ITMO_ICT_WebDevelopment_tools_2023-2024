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


class MessageDefault(SQLModel):
    message: str
    seemed: bool
    subcase_id: Optional[int] = Field(default=None, foreign_key="subcase.id")


class MessagesSubmodels(MessageDefault):
    subcase: Optional["Subcase"] = None


class Message(MessageDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    subcase: Optional["Subcase"] = Relationship(back_populates="messages")


class SubcaseDefault (SQLModel):
    what_to_do: str
    comment: str
    deadline: datetime.datetime
    case_id: Optional[int] = Field(default=None, foreign_key="case.id")


class SubcaseSubmodels(SubcaseDefault):
    case: Optional["Case"] = None
    messages: Optional[List["Message"]] = None


class Subcase(SubcaseDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    case: Optional["Case"] = Relationship(back_populates="subcases")
    messages: Optional[List["Message"]] = Relationship(back_populates="subcase",
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


class Doing(SQLModel,  table=True):
    id: int = Field(default=None, primary_key=True)
    time_spent: datetime.timedelta = datetime.timedelta(seconds=0)

    case_id: Optional[int] = Field(
        default=None, foreign_key="case.id", primary_key=True
    )
    user_id: Optional[int] = Field(
        default=None, foreign_key="user.id", primary_key=True
    )


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


class UserDefault(SQLModel):
    username: str


class UserSubmodels(UserDefault):
    cases: Optional[List["Case"]] = None


class User(UserDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    cases: Optional[List["Case"]] = Relationship(
        back_populates="users", link_model=Doing
    )


class ManyToManyUpdate(BaseModel):
    case_id: int
