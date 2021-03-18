from sqlalchemy.orm import Session

from app.models import User, Team, Project, Column, Task


seed_data = [
    Team(team_name='team1'),
    Team(team_name='team2'),
    Project(project_name='project1', team_id=1),
    Project(project_name='project2', team_id=1),
    Project(project_name='project3', team_id=2),
    Column(column_name='column1', column_pos=0, project_id=1),
    Column(column_name='column2', column_pos=1, project_id=1),
    Column(column_name='column3', column_pos=2, project_id=1),
    Column(column_name='column4', column_pos=3, project_id=1),
    Column(column_name='column5', column_pos=0, project_id=2),
    Column(column_name='column6', column_pos=1, project_id=2),
    Column(column_name='column7', column_pos=0, project_id=3),
    Task(task_description='task1', column_id=0, column_idx=0),
    Task(task_description='task2', column_id=0, column_idx=1),
    Task(task_description='task3', column_id=1, column_idx=0),
    Task(task_description='task4', column_id=1, column_idx=1),
    Task(task_description='task5', column_id=1, column_idx=2),
    Task(task_description='task6', column_id=2, column_idx=0),
    Task(task_description='task7', column_id=3, column_idx=0),
    Task(task_description='task8', column_id=3, column_idx=1),
    Task(task_description='task9', column_id=3, column_idx=2),
    Task(task_description='task10', column_id=4, column_idx=0),
    Task(task_description='task11', column_id=6, column_idx=0),
    Task(task_description='task12', column_id=6, column_idx=1),
    Task(task_description='task13', column_id=6, column_idx=2),
    Task(task_description='task14', column_id=7, column_idx=0),
    Task(task_description='task15', column_id=7, column_idx=1),
    User(first_name='test1', last_name='user1', email='test1@user.com', hashed_password='password', team_id=1),
    User(first_name='test2', last_name='user2', email='test2@user.com', hashed_password='password', team_id=1),
    User(first_name='test3', last_name='user3', email='test3@user.com', hashed_password='password', team_id=1),
    User(first_name='test4', last_name='user4', email='test4@user.com', hashed_password='password', team_id=2)]


def seed_db(db: Session):
    for item in seed_data:
        db.add(item)

    db.commit()
