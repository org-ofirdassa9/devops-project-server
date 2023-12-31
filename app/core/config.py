from pydantic import BaseSettings
from fastapi_jwt_auth import AuthJWT
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = os.environ.get("PROJECT_NAME", "DevOps Project")
    DATABASE_URL: str = os.environ.get("DB_CONN_STRING", "postgresql://postgres:Aa123456@localhost/project")
    authjwt_secret_key: str = os.environ.get("JWT_SECRET_KEY", "your-secret-key")
    # Configure application to store and get JWT from cookies
    authjwt_token_location: set = ('headers','cookies')
    # Only allow JWT cookies to be sent over https
    authjwt_cookie_secure: bool = True # False for local development
    # CSRF Protection.
    authjwt_cookie_csrf_protect: bool = True # False for local development
    # Change to 'lax' in production to make your website more secure from CSRF Attacks, default is None
    authjwt_cookie_samesite: str = 'lax'

settings = Settings()

@AuthJWT.load_config
def get_config():
    return Settings()
