from pydantic import BaseSettings
from fastapi_jwt_auth import AuthJWT

class Settings(BaseSettings):
    PROJECT_NAME: str = "Let Platform Server"
    DATABASE_URL: str = "postgresql://postgres:Aa123456@localhost/let2"
    authjwt_secret_key: str = "your-secret-key"
    # Configure application to store and get JWT from cookies
    authjwt_token_location: set = ('headers','cookies')
    # Only allow JWT cookies to be sent over https
    authjwt_cookie_secure: bool = False
    # Disable CSRF Protection for this example. default is True
    authjwt_cookie_csrf_protect: bool = False
    # Change to 'lax' in production to make your website more secure from CSRF Attacks, default is None
    # authjwt_cookie_samesite: str = 'lax'

settings = Settings()

@AuthJWT.load_config
def get_config():
    return Settings()
