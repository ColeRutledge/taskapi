from typing import Union

from sqlalchemy.orm import Session

from app.models import User, Team, Project, Column, Task
from app.schemas import (
    ColumnBase, ProjectBase, TaskBase, TeamBase, UserCreate, UserUpdate)


# custom types for orm models and pydantic schemas
Model = Union[User, Team, Project, Column, Task]
Schema = Union[UserCreate, UserUpdate, TeamBase, ProjectBase, ColumnBase, TaskBase]


# ############################ CRUD #################################### #

def create(db: Session, schema: Schema, model: Model):
    db_model = model(schema.dict())
    db.add(db_model)
    db.commit()
    db.refresh(db_model)
    return db_model


def read(db: Session, id: int, model: Model):
    return db.query(model).filter(id == model.id).first()


def read_all(db: Session, model: Model, skip: int = 0, limit: int = 100):
    return db.query(model).offset(skip).limit(limit).all()


def update(db: Session, schema: Schema, model: Model):
    schema = schema.dict(exclude_unset=True)
    if isinstance(model, User) and 'password' in schema:
        hashed_password = model.get_password_hash(schema['password'])
        schema['hashed_password'] = hashed_password
        del schema['password']

    db.query(type(model))\
      .filter_by(id=model.id)\
      .update(schema, synchronize_session=False)
    db.commit()
    return model


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
