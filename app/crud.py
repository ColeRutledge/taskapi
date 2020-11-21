from sqlalchemy.orm import Session
from app import models, schemas


# ############################# USER CRUD ############################## #

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + 'notreallyhashed'
    db_user = models.User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        hashed_password=fake_hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, schema: schemas.UserUpdate, model: models.User):
    fake_hashed_password = schema.password + 'notreallyhashed' \
        if schema.password else model.hashed_password
    db.query(models.User)\
      .filter_by(id=model.id)\
      .update({'first_name': schema.first_name or model.first_name,
               'last_name': schema.last_name or model.last_name,
               'email': schema.email or model.email,
               'hashed_password': fake_hashed_password,
               'team_id': schema.team_id or model.team_id},
              synchronize_session=False)
    db.commit()
    return model


def delete_user(db: Session, user: models.User):
    db.delete(user)
    db.commit()
    return user


# ############################ TEAM CRUD ############################### #

def get_team(db: Session, team_id: int):
    return db.query(models.Team).filter(models.Team.id == team_id).first()


def get_teams(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Team).offset(skip).limit(limit).all()


def create_team(db: Session, team: schemas.TeamBase):
    db_team = models.Team(**team.dict())
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team


def update_team(db: Session, schema: schemas.TeamBase, model: models.Team):
    db.query(models.Team)\
      .filter_by(id=model.id)\
      .update({'team_name': schema.team_name or model.team_name},
              synchronize_session=False)
    db.commit()
    return model


def delete_team(db: Session, team: models.Team):
    db.delete(team)
    db.commit()
    return team


# ############################ PROJECT CRUD ############################ #

def get_project(db: Session, project_id: int):
    return db.query(models.Project).filter(models.Project.id == project_id).first()


def get_projects(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Project).offset(skip).limit(limit).all()


def create_project(db: Session, project: schemas.ProjectBase):
    db_project = models.Project(**project.dict())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def update_project(db: Session, schema: schemas.ProjectBase, model: models.Project):
    db.query(models.Project)\
      .filter_by(id=model.id)\
      .update({'project_name': schema.project_name or model.project_name},
              synchronize_session=False)
    db.commit()
    return model


def delete_project(db: Session, project: models.Project):
    db.delete(project)
    db.commit()
    return project


# ############################ COLUMN CRUD ############################# #

def get_column(db: Session, column_id: int):
    return db.query(models.Column).filter(models.Column.id == column_id).first()


def get_columns(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Column).offset(skip).limit(limit).all()


def create_column(db: Session, column: schemas.ColumnBase):
    db_column = models.Column(**column.dict())
    db.add(db_column)
    db.commit()
    db.refresh(db_column)
    return db_column


def update_column(db: Session, schema: schemas.ColumnBase, model: models.Column):
    db.query(models.Column)\
      .filter_by(id=model.id)\
      .update({'column_name': schema.column_name or model.column_name},
              synchronize_session=False)
    db.commit()
    return model


def delete_column(db: Session, column: models.Column):
    db.delete(column)
    db.commit()
    return column


# ############################ TASK CRUD ############################### #

def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()


def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Task).offset(skip).limit(limit).all()


def create_task(db: Session, task: schemas.TaskBase):
    db_task = models.Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task(db: Session, schema: schemas.TaskBase, model: models.Task):
    db.query(models.Task)\
      .filter_by(id=model.id)\
      .update({'task_description': schema.task_description or model.task_description},
              synchronize_session=False)
    db.commit()
    return model


def delete_task(db: Session, task: models.Task):
    db.delete(task)
    db.commit()
    return task
