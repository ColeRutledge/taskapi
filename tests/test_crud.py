import pytest
from sqlalchemy.orm import Session

from app import crud, models, schemas


@pytest.mark.parametrize(
    argnames=['Schema', 'Model', 'schema_vals', 'attributes', 'field', 'value'],
    argvalues=[
        (
            schemas.UserCreate,
            models.User,
            {
                'first_name': 'Test', 'last_name': 'User',
                'email': 'test@user.com', 'password': 'badpassword'},
            ['first_name', 'last_name', 'hashed_password', 'email'],
            'email',
            'test@user.com'),
        (
            schemas.ProjectBase,
            models.Project,
            {'project_name': 'Test', 'team_id': 1},
            ['project_name', 'team_id'],
            'project_name',
            'Test')])
def test_create(
        Schema: crud.Schema,
        Model: crud.DatabaseModel,
        schema_vals: dict,
        attributes: list[str],
        field: str,
        value: str,
        monkeypatch,
        test_db_seeded: Session):

    def mock_get_password_hash(*args):
        return 'fake_hashed_password'

    monkeypatch.setattr(models.User, 'get_password_hash', mock_get_password_hash)

    schema = Schema(**schema_vals)
    orm_model = crud.create(test_db_seeded, schema, Model)
    assert getattr(orm_model, field) == value
    assert all(getattr(orm_model, field, False) for field in attributes)


@pytest.mark.parametrize(
    argnames=['resource_id', 'Model', 'attributes', 'field', 'value'],
    argvalues=[
        (
            1,
            models.User,
            ['first_name', 'last_name', 'hashed_password', 'email'],
            'email',
            'bob@smith.com'),
        (
            2,
            models.Project,
            ['project_name', 'team_id'],
            'project_name',
            'SEO')])
def test_read(
        resource_id: int,
        Model: crud.DatabaseModel,
        attributes: list[str],
        field: str,
        value: str,
        test_db_seeded: Session):

    orm_model = crud.read(test_db_seeded, resource_id, Model)
    assert getattr(orm_model, field) == value
    assert all(getattr(orm_model, field, False) for field in attributes)


@pytest.mark.parametrize(
    argnames=['Model', 'attributes', 'field', 'value', 'length'],
    argvalues=[
        (
            models.User,
            ['first_name', 'last_name', 'hashed_password', 'email'],
            'email',
            'Sally@123.com',
            4),
        (
            models.Project,
            ['project_name', 'team_id'],
            'project_name',
            'SEO',
            3)])
def test_read_all(
        Model: crud.DatabaseModel,
        attributes: list[str],
        field: str,
        value: str,
        length: int,
        test_db_seeded: Session):

    orm_model_list = crud.read_all(test_db_seeded, Model)
    assert len(orm_model_list) == length
    assert getattr(orm_model_list[1], field) == value
    assert all(getattr(orm_model_list[1], field, False) for field in attributes)


@pytest.mark.parametrize(
    argnames=[
        'resource_id',
        'Schema',
        'Model',
        'schema_vals',
        'attributes',
        'field',
        'updated_value'],
    argvalues=[
        (
            1,
            schemas.UserUpdate,
            models.User,
            {'password': 'badpassword'},
            ['first_name', 'last_name', 'hashed_password', 'email'],
            'hashed_password',
            'fake_hashed_password'),
        (
            2,
            schemas.ProjectUpdate,
            models.Project,
            {'project_name': 'Deploy'},
            ['project_name', 'team_id'],
            'project_name',
            'Deploy')])
def test_update(
        resource_id: int,
        Schema: crud.Schema,
        Model: crud.DatabaseModel,
        schema_vals: dict,
        attributes: list[str],
        field: str,
        updated_value: str,
        monkeypatch,
        test_db_seeded: Session):

    def mock_get_password_hash(*args):
        return 'fake_hashed_password'

    monkeypatch.setattr(models.User, 'get_password_hash', mock_get_password_hash)

    schema = Schema(**schema_vals)
    orm_model = crud.read(test_db_seeded, resource_id, Model)
    updated_orm_model = crud.update(test_db_seeded, schema, orm_model)
    assert getattr(updated_orm_model, field) == updated_value
    assert all(getattr(updated_orm_model, field, False) for field in attributes)


@pytest.mark.parametrize(
    argnames=['resource_id', 'Model', 'attributes', 'field', 'value'],
    argvalues=[
        (
            1,
            models.User,
            ['first_name', 'last_name', 'hashed_password', 'email'],
            'email',
            'bob@smith.com'),
        (
            2,
            models.Project,
            ['project_name', 'team_id'],
            'project_name',
            'SEO')])
def test_delete(
        resource_id: int,
        Model: crud.DatabaseModel,
        attributes: list[str],
        field: str,
        value: str,
        test_db_seeded: Session):

    orm_model = crud.read(test_db_seeded, resource_id, Model)
    deleted_orm_model = crud.delete(test_db_seeded, orm_model)
    assert getattr(deleted_orm_model, field) == value
    assert all(getattr(deleted_orm_model, field, False) for field in attributes)
