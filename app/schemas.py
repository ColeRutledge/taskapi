from typing import Optional
from pydantic import BaseModel


class TeamBase(BaseModel):
    team_name: str


class Team(TeamBase):
    id: int


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: str


class UserCreate(BaseModel):
    password: str


class User(UserBase):
    id: int
    team_id: Optional[int] = None
    team: Team
