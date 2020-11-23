from typing import Optional
from pydantic import BaseModel  # create_model
from datetime import datetime


# ######### AUTH ######### #

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


# ######### TEAM ######### #

class TeamBase(BaseModel):
    team_name: str


class Team(TeamBase):
    id: int

    class Config:
        orm_mode = True


# ######### USER ######### #

class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: str


class UserCreate(UserBase):
    password: str


class UserUpdate(UserCreate):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    team_id: Optional[int] = None


class User(UserBase):
    id: int
    team_id: Optional[int] = None

    class Config:
        orm_mode = True


# ######### PROJECT ######### #

class ProjectBase(BaseModel):
    project_name: str
    team_id: int


class Project(ProjectBase):
    id: int

    class Config:
        orm_mode = True


# ######### COLUMN ######### #

class ColumnBase(BaseModel):
    column_name: str
    column_pos: int
    project_id: int


class ColumnUpdate(BaseModel):
    column_name: Optional[str] = None
    column_pos: Optional[int] = None
    project_id: Optional[int] = None


class Column(ColumnBase):
    id: int

    class Config:
        orm_mode = True


# ######### TASK ######### #

class TaskBase(BaseModel):
    task_description: str
    due_date: Optional[datetime] = None
    column_id: int
    column_idx: int


class TaskUpdate(BaseModel):
    task_description: Optional[str] = None
    due_date: Optional[datetime] = None
    column_id: Optional[int] = None
    column_idx: Optional[int] = None


class Task(TaskBase):
    id: int

    class Config:
        orm_mode = True


# class ColumnTasks(BaseModel):
#     Column.column_name: create_model('')


# class ProjectData(Project):
#     data: list[ColumnTasks]


# class Plant(BaseModel):
#     daytime: Optional[create_model('DayTime', sunrise=(int, ...), sunset=(int, ...))] = None  # noqa
#     type: str
