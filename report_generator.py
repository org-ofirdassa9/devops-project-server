from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
import logging
import os
import importlib

logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)
app = FastAPI(
    docs_url=f"/report_generator/docs",
    openapi_url="/report_generator/openapi.json",
    redoc_url=None,
    version="0.0.1",
    title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.CORS_ORIGIN],  # Your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message}
    )


@app.on_event("startup")
async def startup_event():
    logger.info("Starting up the application")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down the application")


# Directory containing your endpoint modules
endpoints_directory = os.path.join(os.path.dirname(__file__), 'app/api/report_generator/endpoints')

# Iterate over each file in the endpoints directory
for filename in os.listdir(endpoints_directory):
    # Filter out non-Python files and __init__.py
    if filename.endswith('.py') and filename != '__init__.py':
        # Remove the file extension to get the module name
        module_name = filename[:-3]

        # Dynamically import the module
        module = importlib.import_module(f'app.api.report_generator.endpoints.{module_name}')

        # Add the router from the imported module
        if hasattr(module, 'router'):
            app.include_router(module.router, prefix=f"/api/report_generator/{module_name}", tags=[module_name])
