from app import config, models
from app.db import engine
from app.routers import users, teams, projects, columns, tasks
from fastapi import FastAPI, Depends
from functools import lru_cache


@lru_cache()
def get_settings():
    return config.Settings()


app = FastAPI()
app_config = get_settings()
models.Base.metadata.create_all(bind=engine)


from app.auth import auth_router
from app.auth.auth_utils import get_current_user


app.include_router(auth_router.router, tags=['Auth'])
app.include_router(
    users.router,
    tags=['Users'], prefix='/users',
    dependencies=[Depends(get_current_user)]
)
app.include_router(
    teams.router,
    tags=['Teams'], prefix='/teams',
    dependencies=[Depends(get_current_user)]
)
app.include_router(
    projects.router,
    tags=['Projects'], prefix='/projects',
    dependencies=[Depends(get_current_user)]
)
app.include_router(
    columns.router,
    tags=['Columns'], prefix='/columns',
    dependencies=[Depends(get_current_user)]
)
app.include_router(
    tasks.router,
    tags=['Tasks'], prefix='/tasks',
    dependencies=[Depends(get_current_user)],
)
