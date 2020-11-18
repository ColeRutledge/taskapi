from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, String, Integer, Table
from sqlalchemy.orm import relationship


Base = declarative_base()

# followers = Table(
#     'teams',
#     Column('follower_id', Integer, ForeignKey('users.id')),
#     Column('followed_id', Integer, ForeignKey('users.id')),
# )


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(20), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String)
    team_id = Column(Integer, ForeignKey('teams.id'))

    team = relationship('Team', back_populates='users')


class Team(Base):
    __tablename__ = 'teams'
    id = Column(Integer, primary_key=True, index=True)
    team_name = Column(String(50), unique=True, index=True, nullable=False)

    users = relationship('User', back_populates='team')
    projects = relationship('Project', back_populates='team', cascade='all, delete-orphan')


class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True, index=True)
    project_name = Column(String(50), unique=True, index=True, nullable=False)
    team_id = Column(Integer, ForeignKey('teams.id'), nullable=False)

    team = relationship('Team', back_populates='projects')
