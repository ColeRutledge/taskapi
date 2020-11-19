from typing import Optional
from pydantic import BaseModel
from datetime import datetime


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


class Task(TaskBase):
    id: int

    class Config:
        orm_mode = True
