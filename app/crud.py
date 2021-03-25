from typing import Union

from sqlalchemy.orm import Session

from app.models import User, Team, Project, Column, Task
from app.schemas import (
    ColumnBase, ProjectBase, TaskBase, TeamBase, UserCreate, UserUpdate)


# custom types for orm models and pydantic schemas
DatabaseModel = Union[User, Team, Project, Column, Task]
Schema = Union[UserCreate, UserUpdate, TeamBase, ProjectBase, ColumnBase, TaskBase]


def create(db: Session, schema: Schema, Model: DatabaseModel):
    schema = schema.dict()
    if Model == User:
        hashed_password = Model.get_password_hash(schema['password'])
        schema['hashed_password'] = hashed_password
        del schema['password']

    db_model = Model(**schema)
    db.add(db_model)
    db.commit()
    db.refresh(db_model)
    return db_model


def read(db: Session, id: int, model: DatabaseModel):
    return db.query(model).filter(id == model.id).first()


def read_all(db: Session, model: DatabaseModel, skip: int = 0, limit: int = 100):
    return db.query(model).offset(skip).limit(limit).all()


def update(db: Session, schema: Schema, model: DatabaseModel):
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


def delete(db: Session, model: DatabaseModel):
    db.delete(model)
    db.commit()
    return model
