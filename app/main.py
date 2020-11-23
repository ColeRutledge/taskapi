from app import config, models
from app.db import engine
from app.routers import users, teams, projects, columns, tasks
from fastapi import FastAPI
from functools import lru_cache


@lru_cache()
def get_settings():
    return config.Settings()


models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app_config = get_settings()

app.include_router(users.router, tags=['Users'], prefix='/users')
app.include_router(teams.router, tags=['Teams'], prefix='/teams')
app.include_router(projects.router, tags=['Projects'], prefix='/projects')
app.include_router(columns.router, tags=['Columns'], prefix='/columns')
app.include_router(tasks.router, tags=['Tasks'], prefix='/tasks')
