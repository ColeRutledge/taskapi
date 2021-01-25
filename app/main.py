from app import config, models
from app.db import engine
from app.tag_meta import tags_metadata
from fastapi import FastAPI, Depends, templating, responses, Request, staticfiles
from app.auth import auth_router
from app.auth.auth_utils import get_current_user
from app.routers import users, teams, projects, columns, tasks


app = FastAPI(
    title='Asana FastAPI',
    description='FastAPI Python server for an Asana clone',
    openapi_tags=tags_metadata,
)
app_config = config.get_settings()
models.Base.metadata.create_all(bind=engine)
templates = templating.Jinja2Templates(directory='app/templates')


app.mount('/static', staticfiles.StaticFiles(directory='app/static'), name='static')


@app.get('/', response_class=responses.HTMLResponse)
async def user_login(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


@app.get("/items/{id}", response_class=responses.HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse("item.html", {"request": request, "id": id})


app.include_router(auth_router.router, tags=['Auth'])
app.include_router(
    users.router,
    tags=['Users'], prefix='/users',
    # dependencies=[Depends(get_current_user)],
)
app.include_router(
    teams.router,
    tags=['Teams'], prefix='/teams',
    dependencies=[Depends(get_current_user)],
)
app.include_router(
    projects.router,
    tags=['Projects'], prefix='/projects',
    dependencies=[Depends(get_current_user)],
)
app.include_router(
    columns.router,
    tags=['Columns'], prefix='/columns',
    dependencies=[Depends(get_current_user)],
)
app.include_router(
    tasks.router,
    tags=['Tasks'], prefix='/tasks',
    dependencies=[Depends(get_current_user)],
)
