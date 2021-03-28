<h2 style="margin: 3%" align='center'>Thanks for checking out my project! 👋</h2>
<h3 style="margin: 3%" align='center'>This is a FastAPI Python server for powering a task management application based on Asana</h3>

<p style="margin: 3%" align='center'>
    <img src="https://github.com/ColeRutledge/asana_fastapi/actions/workflows/ci.yml/badge.svg?branch=master" alt="Continuous Integration and Delivery">
    <img src="https://img.shields.io/badge/Test%20Coverage-100%25-brightgreen" alt="Test Coverage">
</p>

<p style="margin: 3%" align='center'>
    <a href='https://asana-fastapi.herokuapp.com/docs' target='_blank'>Link to live API Docs powered by OpenAPI</a>
</p>

<p style="margin: 3%">I had a great time making this app over the course of a few weeks. To build on my experience from the App Academy bootcamp, I really tried to expand on my "infrastructure as code" skills by utilizing multistage Docker builds, layered caching, and Github Actions to build a simple CI/CD pipeline. It was immensely satisfying glueing the pieces of it together with the Python skills I've been developing over the prior few months and to see it become a more robust, maintainable project complete with 💯 percent test coverage! (not a great metric, I know, but it was still fun to chase!)</p>

### Takeways:

<ul style="margin: 3%">
    <li>Infrastructure as code is <b>EXCITING</b>... serverless, lambdas, containers, <b>YES!</b> 🎉</li>
    <li>GitHub Actions are going in <b>every</b>.<b>single</b>.<b>project.</b> ✔</li>
    <li>pytest is powerful! 💪 fixtures, parametrized testing, and monkeypatching were all absurdly helpful.</li>
    <li>I'm firmly in the "pro-type hints" camp now.</li>
    <li>For simple projects, I doubt I'll look for a web framework outside of <a href='https://github.com/tiangolo/fastapi' target='_blank'>FastAPI</a> for a long time. I learned more from <a href='https://github.com/tiangolo' target='_blank'>tiangolo's</a> documentation than I did from several weeks of bootcamp material. Thank you, Sebastián!  🙌</li>
    <li>you can also thank him for the overzealous use of emojis as well! 😀 </li>
</ul>

### Usage:

<p style="margin: 3%">I have prepared a docker-compose file, so after cloning, you should only need to setup a few environment variables. The Pydantic config schema in app.config provides valid defaults for all of these, but the required environment variables are: </p>

```bash
APP_NAME="asana_fastapi"
DB_URL="sqlite:///app.db"
SECRET_KEY="dummykey"
ALGORITHM="HS256"                   # password hashing algorithm
ACCESS_TOKEN_EXPIRES_MINUTES=30     # auth token expiration
```

<p style="margin: 3%">Alternatively, you can just pull the <b>dev</b> or <b>prod</b> <a href='https://github.com/users/ColeRutledge/packages/container/package/asana_fastapi'>image</a> from the GitHub Container Registry for this project, and run it by using one of these commands with the Docker CLI installed: </p>

```bash
docker run --name ${APP_NAME} -p 8000:80 -d --rm ghcr.io/colerutledge/asana_fastapi:dev
docker run --name ${APP_NAME} -p 8000:80 -d --rm ghcr.io/colerutledge/asana_fastapi:prod
```
