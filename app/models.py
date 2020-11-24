from app.db import get_db
from fastapi import Depends
from passlib.context import CryptContext
from sqlalchemy.ext.declarative import declarative_base  # declared_attr
from sqlalchemy import Column as DB_Column, ForeignKey, String, Integer, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import func


Base = declarative_base()
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class TimestampMixin(object):
    # will need to adjust the ordering of columns in the migration file
    created_on = DB_Column(DateTime, server_default=func.now())
    updated_on = DB_Column(
        DateTime,
        server_default=func.now(),
        server_onupdate=func.now()
    )
    # by using declared_attr here, we can force
    # created_on and updated_on to end of db table
    # @declared_attr
    # def created_on(cls):
    #     return DB_Column(DateTime, server_default=func.now())

    # @declared_attr
    # def updated_on(cls):
    #     return DB_Column(
    #         DateTime,
    #         server_default=func.now(),
    #         server_onupdate=func.now()
    #     )


class User(Base, TimestampMixin):
    __tablename__ = 'users'

    id = DB_Column(Integer, primary_key=True, index=True)
    first_name = DB_Column(String(20), nullable=False)
    last_name = DB_Column(String(50), nullable=False)
    email = DB_Column(String, unique=True, index=True, nullable=False)
    hashed_password = DB_Column(String)
    team_id = DB_Column(Integer, ForeignKey('teams.id'))

    team = relationship('Team', back_populates='users')

    def get_password_hash(self, password):
        return pwd_context.hash(password)

    @staticmethod
    def get_user_by_email(db: Session, email: str):
        return db.query(User)\
                 .filter(func.lower(User.email) == func.lower(email))\
                 .first()

    # utility function to authenticate and return a user. OAuth spec
    # requires username vs email while crud is looking up a user via email
    @staticmethod
    def authenticate_user(username: str, password: str,
                          db: Session = Depends(get_db)):
        user: User = User.get_user_by_email(db=db, email=username)
        return user if user and \
            pwd_context.verify(password, user.hashed_password) else False


class Team(Base, TimestampMixin):
    __tablename__ = 'teams'

    id = DB_Column(Integer, primary_key=True, index=True)
    team_name = DB_Column(String(50), unique=True, index=True, nullable=False)

    users = relationship('User', back_populates='team')
    projects = relationship(
        'Project',
        back_populates='team',
        cascade='all, delete-orphan',
    )


class Project(Base, TimestampMixin):
    __tablename__ = 'projects'

    id = DB_Column(Integer, primary_key=True, index=True)
    project_name = DB_Column(String(50), unique=True, index=True, nullable=False)
    team_id = DB_Column(Integer, ForeignKey('teams.id'), nullable=False)

    team = relationship('Team', back_populates='projects')
    columns = relationship(
        'Column',
        back_populates='project',
        cascade='all, delete-orphan',
    )

    def get_project_data(self):
        return [{column.column_name: column.tasks} for column in self.columns]


class Column(Base, TimestampMixin):
    __tablename__ = 'columns'

    id = DB_Column(Integer, primary_key=True, index=True)
    column_name = DB_Column(String(50), unique=True, index=True, nullable=False)
    column_pos = DB_Column(Integer, nullable=False)
    project_id = DB_Column(Integer, ForeignKey('projects.id'), nullable=False)

    project = relationship('Project', back_populates='columns')
    tasks = relationship('Task', back_populates='column', cascade='all, delete-orphan')


class Task(Base, TimestampMixin):
    __tablename__ = 'tasks'

    id = DB_Column(Integer, primary_key=True, index=True)
    task_description = DB_Column(String(255), nullable=False)
    due_date = DB_Column(DateTime)
    column_id = DB_Column(Integer, ForeignKey('columns.id'), nullable=False)
    column_idx = DB_Column(Integer, nullable=False)

    column = relationship('Column', back_populates='tasks')
