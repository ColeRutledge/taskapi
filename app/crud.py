from typing import Union

from sqlalchemy.orm import Session

from app.models import User, Team, Project, Column, Task
from app.schemas import (
    ColumnBase, ProjectBase, TaskBase, TeamBase, UserCreate, UserUpdate)


# custom types for orm models and pydantic schemas
Model = Union[User, Team, Project, Column, Task]
Schema = Union[UserCreate, TeamBase, ProjectBase, ColumnBase, TaskBase]


# ############################ CRUD #################################### #

def create(db: Session, body: Schema, model: Model):
    db_model = model(**body.dict())
    db.add(db_model)
    db.commit()
    db.refresh(db_model)
    return db_model


def read(db: Session, id: int, model: Model):
    return db.query(model).filter(id == model.id).first()


def read_all(db: Session, model: Model, skip: int = 0, limit: int = 100):
    return db.query(model).offset(skip).limit(limit).all()


def delete(db: Session, resource: Model):
    db.delete(resource)
    db.commit()
    return resource


# ############################ USER ############################### #

def create_user(db: Session, user: UserCreate):
    db_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email)
    db_user.hashed_password = db_user.get_password_hash(user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, schema: UserUpdate, model: User):
    fake_hashed_password = schema.password + 'notreallyhashed' \
        if schema.password else model.hashed_password
    db.query(User)\
      .filter_by(id=model.id)\
      .update({'first_name': schema.first_name or model.first_name,
               'last_name': schema.last_name or model.last_name,
               'email': schema.email or model.email,
               'hashed_password': fake_hashed_password,
               'team_id': schema.team_id or model.team_id},
              synchronize_session=False)
    db.commit()
    return model


# ############################ TEAM ############################### #

def update_team(db: Session, schema: TeamBase, model: Team):
    db.query(Team)\
      .filter_by(id=model.id)\
      .update({'team_name': schema.team_name or model.team_name},
              synchronize_session=False)
    db.commit()
    return model


# ############################ PROJECT ############################ #

def update_project(db: Session, schema: ProjectBase, model: Project):
    db.query(Project)\
      .filter_by(id=model.id)\
      .update({'project_name': schema.project_name or model.project_name,
               'team_id': schema.team_id or model.team_id},
              synchronize_session=False)
    db.commit()
    return model


# ############################ COLUMN ############################# #

def update_column(db: Session, schema: ColumnBase, model: Column):
    db.query(Column)\
      .filter_by(id=model.id)\
      .update({'column_name': schema.column_name or model.column_name,
               'column_pos': schema.column_pos or model.column_pos,
               'project_id': schema.project_id or model.project_id},
              synchronize_session=False)
    db.commit()
    return model


# ############################ TASK ############################### #

def update_task(db: Session, schema: TaskBase, model: Task):
    db.query(Task)\
      .filter_by(id=model.id)\
      .update({'task_description': schema.task_description or model.task_description,
               'due_date': schema.due_date or model.due_date,
               'column_id': schema.column_id or model.column_id,
               'column_idx': schema.column_idx or model.column_idx},
              synchronize_session=False)
    db.commit()
    return model
