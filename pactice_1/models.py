import datetime
from pydantic import BaseModel
from enum import Enum
from typing import Optional, List

class Priority(Enum):
    super_high = "super_high"
    high = "high"
    normal = "normal"
    low = "low"
    super_low = "super_low"


class Subcase(BaseModel):
    id: int
    what_to_do: str
    comment: str
    deadline: datetime.datetime


class Case(BaseModel):
    id: int
    name: str
    description: str
    priority: Priority
    subcases: Optional[List[Subcase]] = []


class Doing(BaseModel):
    id: int
    case: Case
    time_spent: int


class Message(BaseModel):
    id: int
    seemed: bool
    subcase: Subcase


class User(BaseModel):
    id: int
    username: str
    doing: Optional[List[Doing]] = []
