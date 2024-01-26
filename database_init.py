from app.core.database import engine
from app.models.models import Base  # Import Base from your user model
from app.models.models import User, HealthMetrics
from app.core.database import SessionLocal
import logging

logger = logging.getLogger(__name__)

def init_db():
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created.")
     # Creating a sample user
    sample_user = User(
        email="sample@example.com",
        hashed_password="Aa123456!",
        first_name="John",
        last_name="Doe",
        registration_date="2024-01-26",  # Add a valid date here
        isAdmin=False
    )

    # Creating sample health metrics for the user
    sample_health_metrics = HealthMetrics(
        heart_rate=70,
        blood_pressure=120/80,
        body_temperature=98.6,
        blood_sugar_level=100.5,
        min_heart_rate=60,
        max_heart_rate=80,
        min_blood_pressure=110/70,
        max_blood_pressure=130/90,
        min_body_temperature=97.0,
        max_body_temperature=99.0,
        min_blood_sugar_level=90.0,
        max_blood_sugar_level=110.0,
    )

    # Associate the health metrics with the user
    sample_user.health_metrics.append(sample_health_metrics)

    # Add the sample user and health metrics to the database
    db = SessionLocal()
    db.add(sample_user)
    db.commit()
    db.close()

    logger.info("Sample user and health metrics added to the database.")

if __name__ == "__main__":
    init_db()
