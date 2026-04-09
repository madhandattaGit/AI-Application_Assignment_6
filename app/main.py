import logging

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.router import api_router
from app.core.config import settings

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(_, exc: RequestValidationError) -> JSONResponse:
        details = [
            f"{'.'.join(str(part) for part in error['loc'] if part != 'body')}: {error['msg']}"
            if any(part != "body" for part in error["loc"])
            else error["msg"]
            for error in exc.errors()
        ]
        return JSONResponse(
            status_code=422,
            content={"error": "Invalid request payload", "details": details},
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(_, exc: Exception) -> JSONResponse:
        logger.exception("Unhandled application error", exc_info=exc)
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal server error",
                "details": ["An unexpected error occurred while processing the request."],
            },
        )

    return app


app = create_app()
