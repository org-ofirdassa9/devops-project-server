from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi.middleware.cors import CORSMiddleware
from app.api.api_v1.endpoints import user
from app.core.config import settings
import logging

# setup loggers
logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)
app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Your frontend's URL
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

app.include_router(user.router, prefix="/api/v1/users", tags=["users"])
