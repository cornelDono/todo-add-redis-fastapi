from fastapi import FastAPI

from application.api.routes.healthcheck import router as healthcheck_router

def create_app() -> FastAPI:
    app = FastAPI(
        title='Simple ToDo app with Reddis',
        docs_url='/',
        description='A Simple ToDo app',
        debug=True,
    )

    app.include_router(healthcheck_router, prefix='/healthcheck')
    return app
