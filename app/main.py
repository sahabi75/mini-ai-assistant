"""FastAPI application entrypoint."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.v1.router import api_router
from app.core.config import get_settings
from app.core.exceptions import AppError, ExternalServiceError, NotFoundError, ValidationError
from app.core.logging_config import get_logger, setup_logging
from app.tools.order_status_tool import OrderStatusTool
from app.tools.product_search_tool import ProductSearchTool
from app.tools.registry import register_tool

setup_logging()
logger = get_logger(__name__)
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Run startup logic before the app accepts requests, and cleanup after."""
    logger.info("Starting %s in '%s' environment", settings.app_name, settings.app_env)
    register_tool(OrderStatusTool())
    register_tool(ProductSearchTool())
    yield
    logger.info("Shutting down %s", settings.app_name)


app = FastAPI(
    title=settings.app_name,
    description="Mini AI Assistant API",
    version="0.1.0",
    lifespan=lifespan,
)
app.include_router(api_router)


@app.exception_handler(ValidationError)
async def validation_error_handler(request: Request, exc: ValidationError) -> JSONResponse:
    logger.warning("Validation error on %s: %s", request.url.path, exc.message)
    return JSONResponse(status_code=400, content={"detail": exc.message})


@app.exception_handler(NotFoundError)
async def not_found_error_handler(request: Request, exc: NotFoundError) -> JSONResponse:
    logger.warning("Not found error on %s: %s", request.url.path, exc.message)
    return JSONResponse(status_code=404, content={"detail": exc.message})


@app.exception_handler(ExternalServiceError)
async def external_service_error_handler(request: Request, exc: ExternalServiceError) -> JSONResponse:
    logger.error("External service error on %s: %s", request.url.path, exc.message)
    return JSONResponse(status_code=502, content={"detail": exc.message})


@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    logger.error("Unhandled app error on %s: %s", request.url.path, exc.message)
    return JSONResponse(status_code=500, content={"detail": exc.message})


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled exception on %s", request.url.path)
    return JSONResponse(status_code=500, content={"detail": "An unexpected error occurred."})