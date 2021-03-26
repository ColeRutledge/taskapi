import pytest
from sqlalchemy.orm import Session

from app import crud, models, schemas


@pytest.mark.parametrize(
    argnames=['Schema', 'Model', 'schema_vals', 'attributes', 'field', 'value'],
    argvalues=[
        (schemas.UserCreate, models.User, {
            'first_name': 'Test', 'last_name': 'User',
            'email': 'test@user.com', 'password': 'badpassword'},
         ['first_name', 'last_name', 'hashed_password', 'email'],
         'email', 'test@user.com'),
        (schemas.ProjectBase, models.Project, {
            'project_name': 'Test', 'team_id': 1},
         ['project_name', 'team_id'], 'project_name', 'Test')])
def test_create(
        Schema: crud.Schema,
        Model: crud.DatabaseModel,
        schema_vals: dict,
        attributes: list[str],
        field: str,
        value: str,
        monkeypatch,
        test_db_seeded: Session):

    schema = Schema(**schema_vals)

    def mock_get_password_hash(password):
        return 'fake_hashed_password'

    monkeypatch.setattr(models.User, 'get_password_hash', mock_get_password_hash)
    orm_model = crud.create(test_db_seeded, schema, Model)
    assert getattr(orm_model, field) == value
    assert all(getattr(orm_model, field, False) for field in attributes)


@pytest.mark.parametrize(
    argnames=['resource_id', 'Model', 'attributes', 'field', 'value'],
    argvalues=[
        (1, models.User, [
            'first_name', 'last_name', 'hashed_password', 'email'],
         'email', 'bob@smith.com'),
        (2, models.Project, ['project_name', 'team_id'], 'project_name', 'SEO')])
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
        (models.User, [
            'first_name', 'last_name', 'hashed_password', 'email'],
         'email', 'Sally@123.com', 4),
        (models.Project, ['project_name', 'team_id'], 'project_name', 'SEO', 3)])
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
