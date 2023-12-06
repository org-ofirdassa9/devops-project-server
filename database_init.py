from app.core.database import engine
from app.models.user_model import Base  # Import Base from your user model
import logging

logger = logging.getLogger(__name__)

def init_db():
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created.")

if __name__ == "__main__":
    init_db()
