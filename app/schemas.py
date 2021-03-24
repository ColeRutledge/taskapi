from datetime import datetime
from typing import Optional

from pydantic import BaseModel  # create_model


# ######### AUTH ######### #

class Token(BaseModel):
    access_token: str
    token_type: str


# OAuth spec requires username vs email
class TokenData(BaseModel):
    username: Optional[str] = None


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
    disabled: Optional[bool] = None


class User(UserBase):
    id: int
    team_id: Optional[int] = None
    disabled: Optional[bool] = None
    # hashed_password: str

    class Config:
        orm_mode = True


# ######### PROJECT ######### #

class ProjectBase(BaseModel):
    project_name: str
    team_id: int


class ProjectUpdate(BaseModel):
    project_name: Optional[str] = None
    team_id: Optional[int] = None


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


class ProjectData(BaseModel):
    project_data: dict[str, list[Task]]

    class Config:
        schema_extra = {
            'example': {
                'project_data': {
                    "Pending": [{
                            "id": 1,
                            "task_description": "Research",
                            "column_id": 1,
                            "column_idx": 0,
                            "due_date": "2021-03-23T20:37:32.493Z"}, {
                            "id": 2,
                            "task_description": "Due diligence",
                            "column_id": 1,
                            "column_idx": 1,
                            "due_date": "2021-03-23T20:37:32.493Z"}],
                    "Done": [{
                            "id": 3,
                            "task_description": "A+B Testing",
                            "column_id": 2,
                            "column_idx": 0,
                            "due_date": "2021-03-23T20:37:32.493Z"}, {
                            "id": 4,
                            "task_description": "Sampling",
                            "column_id": 2,
                            "column_idx": 1,
                            "due_date": "2021-03-23T20:37:32.493Z"}]}}}
