from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models import Column, Project, Task


def test_lists_are_limited_to_the_authenticated_team(
        test_app: TestClient,
        test_db_seeded: Session):
    assert {
        project['team_id']
        for project in test_app.get('/projects/').json()
    } == {1}
    assert {
        team['id']
        for team in test_app.get('/teams/').json()
    } == {1}
    assert {
        column['project_id']
        for column in test_app.get('/columns/').json()
    } <= {1, 2}
    assert test_app.get('/users/').json()
    assert all(
        user['team_id'] == 1
        for user in test_app.get('/users/').json()
    )


def test_other_team_resources_cannot_be_read(
        test_app: TestClient,
        test_db_seeded: Session):
    project = test_db_seeded.query(Project).filter_by(team_id=2).first()
    column = test_db_seeded.query(Column).filter_by(
        project_id=project.id).first()
    task = test_db_seeded.query(Task).filter_by(
        column_id=column.id).first()

    responses = [
        test_app.get(f'/projects/{project.id}'),
        test_app.get(f'/projects/{project.id}/data'),
        test_app.get(f'/projects/{project.id}/columns'),
        test_app.get(f'/columns/{column.id}'),
        test_app.get(f'/columns/{column.id}/tasks'),
        test_app.get(f'/tasks/{task.id}'),
        test_app.get('/teams/2'),
        test_app.get('/teams/2/projects'),
        test_app.get('/teams/2/users'),
        test_app.get('/users/4'),
        test_app.get('/users/4/team'),
    ]

    assert all(
        response.status_code == status.HTTP_404_NOT_FOUND
        for response in responses
    )


def test_other_team_resources_cannot_be_modified(
        test_app: TestClient,
        test_db_seeded: Session):
    project = test_db_seeded.query(Project).filter_by(team_id=2).first()
    column = test_db_seeded.query(Column).filter_by(
        project_id=project.id).first()
    task = test_db_seeded.query(Task).filter_by(
        column_id=column.id).first()

    responses = [
        test_app.put(
            f'/projects/{project.id}',
            json={'project': {'project_name': 'Changed'}}),
        test_app.delete(f'/projects/{project.id}'),
        test_app.put(
            f'/columns/{column.id}',
            json={'column': {'column_name': 'Changed'}}),
        test_app.delete(f'/columns/{column.id}'),
        test_app.put(
            f'/tasks/{task.id}',
            json={'task': {'task_description': 'Changed'}}),
        test_app.delete(f'/tasks/{task.id}'),
        test_app.put(
            '/teams/2',
            json={'team': {'team_name': 'Changed'}}),
        test_app.delete('/teams/2'),
        test_app.put(
            '/users/4',
            json={'user_schema': {'first_name': 'Changed'}}),
    ]

    assert all(
        response.status_code == status.HTTP_404_NOT_FOUND
        for response in responses[:8]
    )
    assert responses[8].status_code == status.HTTP_401_UNAUTHORIZED
    test_db_seeded.expire_all()
    assert test_db_seeded.query(Project).get(project.id).project_name == (
        project.project_name)


def test_cannot_create_or_move_resources_into_another_team(
        test_app: TestClient,
        test_db_seeded: Session):
    foreign_project = test_db_seeded.query(Project).filter_by(team_id=2).first()
    own_project = test_db_seeded.query(Project).filter_by(team_id=1).first()
    foreign_column = test_db_seeded.query(Column).filter_by(
        project_id=foreign_project.id).first()
    own_column = test_db_seeded.query(Column).filter_by(
        project_id=own_project.id).first()
    own_task = test_db_seeded.query(Task).filter_by(
        column_id=own_column.id).first()

    responses = [
        test_app.post(
            '/projects/',
            json={'project_name': 'Foreign', 'team_id': 2}),
        test_app.put(
            f'/projects/{own_project.id}',
            json={'project': {'team_id': 2}}),
        test_app.post(
            '/columns/',
            json={
                'column_name': 'Foreign',
                'column_pos': 0,
                'project_id': foreign_project.id,
            }),
        test_app.put(
            f'/columns/{own_column.id}',
            json={'column': {'project_id': foreign_project.id}}),
        test_app.post(
            '/tasks/',
            json={
                'task_description': 'Foreign',
                'column_idx': 0,
                'column_id': foreign_column.id,
            }),
        test_app.put(
            f'/tasks/{own_task.id}',
            json={'task': {'column_id': foreign_column.id}}),
        test_app.put(
            '/users/1',
            json={'user_schema': {'team_id': 2}}),
    ]

    assert all(
        response.status_code == status.HTTP_404_NOT_FOUND
        for response in responses
    )
