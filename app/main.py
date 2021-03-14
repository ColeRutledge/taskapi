from fastapi import FastAPI, Depends, templating, responses, Request, staticfiles

from app.tag_meta import tags_metadata
from app.auth import auth_router
from app.auth.auth_utils import get_current_user
from app.routers import users, teams, projects, columns, tasks


def create_application() -> FastAPI:
    application = FastAPI(
        title='Asana FastAPI',
        openapi_tags=tags_metadata,
        description='FastAPI Python server for an Asana clone')
    application.mount(
        path='/static', name='static',
        app=staticfiles.StaticFiles(directory='app/static'))

    application.include_router(auth_router.router, tags=['Auth'])
    application.include_router(users.router, tags=['Users'], prefix='/users')

    protected_routers = [
        (teams.router, 'Teams', '/teams'),
        (projects.router, 'Projects', '/projects'),
        (columns.router, 'Columns', '/columns'),
        (tasks.router, 'Tasks', '/tasks')]
    for router, tag, prefix in protected_routers:
        application.include_router(
            router=router, tags=[tag], prefix=prefix,
            dependencies=[Depends(get_current_user)])

    return application


app = create_application()

templates = templating.Jinja2Templates(directory='app/templates')


@app.get('/', response_class=responses.HTMLResponse)
async def user_login(request: Request):
    return templates.TemplateResponse(
        'index.html', {'request': request, 'request_headers': request._headers._list})


@app.get('/items/{id}', response_class=responses.HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse("item.html", {"request": request, "id": id})
