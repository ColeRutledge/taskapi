import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models import Task


@pytest.mark.parametrize(
    'path',
    [
        '/projects/',
        '/columns/',
        '/tasks/',
        '/teams/',
        '/users/',
        '/teams/1/projects',
        '/teams/1/users',
        '/projects/1/columns',
        '/columns/1/tasks',
    ],
)
def test_list_endpoints_accept_offset_and_limit(
        path: str,
        test_app: TestClient,
        test_db_seeded: Session):
    response = test_app.get(path, params={'skip': 1, 'limit': 1})

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1


@pytest.mark.parametrize(
    'params',
    [
        {'skip': -1},
        {'limit': 0},
        {'limit': 101},
    ],
)
def test_list_endpoints_reject_invalid_pagination(
        params: dict,
        test_app: TestClient,
        test_db_seeded: Session):
    response = test_app.get('/tasks/', params=params)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_nested_list_rejects_limit_above_maximum(
        test_app: TestClient,
        test_db_seeded: Session):
    response = test_app.get(
        '/columns/1/tasks',
        params={'limit': 101})

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_empty_list_and_offset_return_empty_arrays(
        test_app: TestClient,
        test_db: Session):
    assert test_app.get('/tasks/').json() == []
    assert test_app.get(
        '/tasks/',
        params={'skip': 20, 'limit': 10},
    ).json() == []


def test_task_pages_include_final_partial_page_and_keep_array_shape(
        test_app: TestClient,
        test_db_seeded: Session):
    test_db_seeded.add_all([
        Task(
            task_description=f'Additional task {index}',
            column_id=1,
            column_idx=index,
        )
        for index in range(105)
    ])
    test_db_seeded.commit()

    first_page = test_app.get('/tasks/').json()
    final_page = test_app.get(
        '/tasks/',
        params={'skip': 100, 'limit': 100},
    ).json()
    expected_ids = [
        task.id
        for task in test_db_seeded.query(Task).order_by(Task.id).all()
    ]
    paged_ids = [
        task['id']
        for task in first_page + final_page
    ]

    assert len(first_page) == 100
    assert len(final_page) == 20
    assert isinstance(first_page, list)
    assert isinstance(final_page, list)
    assert paged_ids == expected_ids
