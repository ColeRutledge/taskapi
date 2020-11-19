from typing import Optional
from pydantic import BaseModel
from sqlalchemy.sql.sqltypes import DateTime


class Team(BaseModel):
    id: int
    team_name: str

    class Config:
        orm_mode = True


class User(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    password: str
    team_id: Optional[int] = None

    class Config:
        orm_mode = True


class Project(BaseModel):
    id: int
    project_name: str
    team_id: int

    class Config:
        orm_mode = True


class Column(BaseModel):
    id: int
    column_name: str
    column_pos: int
    project_id: int

    class Config:
        orm_mode = True


class Task(BaseModel):
    id: int
    task_description: str
    due_date: Optional[DateTime] = None
    column_id: int
    column_idx: int

    class Config:
        orm_mode = True

# class TeamBase(BaseModel):
#     team_name: str


# class Team(TeamBase):
#     id: int


# class UserBase(BaseModel):
#     first_name: str
#     last_name: str
#     email: str


# class UserCreate(BaseModel):
#     password: str


# class User(UserBase):
#     id: int
#     team_id: Optional[int] = None
#     team: Team
