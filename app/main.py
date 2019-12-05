import logging

from fastapi import FastAPI

from . import __version__, api, config, solver, views

log = logging.getLogger(__name__)   # pylint: disable=invalid-name


def create_app():
    app_ = FastAPI(  # pylint: disable=invalid-name
        title='Math Service',
        description='Math service',
        version=__version__,
    )
    app_.include_router(api.router)
    app_.include_router(views.router)

    @app_.on_event("startup")
    def startup():
        app_.solver = solver.Solver(
            max_workers=config.MAX_WORKERS,
            timeout=config.WORKER_TASK_TIMEOUT
        )

    @app_.on_event("shutdown")
    def shutdown():
        app_.solver._process_pool.terminate()
        app_.solver._process_pool.join()

    return app_


app = create_app()
