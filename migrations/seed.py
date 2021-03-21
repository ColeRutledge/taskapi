#!/usr/bin/env python3
import logging

from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.orm import Session

from app.models import User, Team, Project, Column, Task


logger = logging.getLogger(__name__)


def seed_db(db: Session):
    seed_data = [
        Team(team_name='Marketing'),
        Team(team_name='Engineering'),
        Project(team_id=1, project_name='Advertisement'),
        Project(team_id=1, project_name='SEO'),
        Project(team_id=2, project_name='API v2'),
        Column(column_pos=0, project_id=1, column_name='Preproduction'),
        Column(column_pos=1, project_id=1, column_name='Processing'),
        Column(column_pos=2, project_id=1, column_name='Postproduction'),
        Column(column_pos=3, project_id=1, column_name='Final'),
        Column(column_pos=0, project_id=2, column_name='To do'),
        Column(column_pos=0, project_id=3, column_name='Pre-process'),
        Column(column_pos=1, project_id=3, column_name='Post-process'),
        Task(column_id=1, column_idx=0, task_description='Research'),
        Task(column_id=1, column_idx=1, task_description='Due diligence'),
        Task(column_id=2, column_idx=0, task_description='A+B Testing'),
        Task(column_id=2, column_idx=1, task_description='Sampling'),
        Task(column_id=2, column_idx=2, task_description='Filming'),
        Task(column_id=3, column_idx=0, task_description='Casting'),
        Task(column_id=4, column_idx=0, task_description='Budget'),
        Task(column_id=4, column_idx=1, task_description='Design campaign'),
        Task(column_id=4, column_idx=2, task_description='Hire production crew'),
        Task(column_id=5, column_idx=0, task_description='Use Google'),
        Task(column_id=6, column_idx=0, task_description='Write application'),
        Task(column_id=6, column_idx=1, task_description='Profit'),
        Task(column_id=7, column_idx=0, task_description='Gather requirements'),
        Task(column_id=7, column_idx=1, task_description='Design specs'),
        Task(column_id=7, column_idx=2, task_description='Hire engineers'),
        User(first_name='Bob', last_name='Smith', email='bob@smith.com', hashed_password='password', team_id=1),
        User(first_name='Sally', last_name='McBeth', email='Sally@123.com', hashed_password='password', team_id=1),
        User(first_name='John', last_name='Applebaum', email='johnnyA@user.com', hashed_password='password', team_id=1),
        User(first_name='Bill', last_name='McSorley', email='billy-max@rocks.com', hashed_password='password', team_id=2)]

    try:
        db.add_all(seed_data)
        db.commit()
        logger.info('database seed complete.')
    except (IntegrityError, OperationalError) as e:  # if data already exists
        logger.warning(e.orig)
        logger.info('data already exists. skipping seed.')


if __name__ == '__main__':
    import os
    from logging.config import dictConfig
    from app import db, config

    os.makedirs('logs', exist_ok=True)
    dictConfig(config.LOGGING_CONFIG)

    db_session = Session(autocommit=False, autoflush=False, bind=db.engine)
    seed_db(db_session)
    db_session.close()
