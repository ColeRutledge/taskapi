from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy.orm import relationship


Base = declarative_base()


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
    team_name = Column(String, unique=True, index=True, nullable=False)

    users = relationship('User', back_populates='team')
