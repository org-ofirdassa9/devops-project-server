from typing import Dict
from app.models.models import HealthMetrics
from typing import Dict, List
from sqlalchemy.orm import Session


def generate_overview_report(user_id: int, db: Session) -> Dict[str, float]:
    user_health_metrics = db.query(HealthMetrics).filter(HealthMetrics.user_id == user_id).first()
    if not user_health_metrics:
        return {}  # No metrics found for the user

    overview_report = {
        'heart_rate': user_health_metrics.heart_rate,
        'blood_pressure': user_health_metrics.blood_pressure,
        'body_temperature': user_health_metrics.body_temperature,
        'blood_sugar_level': user_health_metrics.blood_sugar_level,
    }
    return overview_report


def generate_min_max_report(user_id: int, db: Session) -> Dict[str, List[float]]:
    user_health_metrics_history = db.query(HealthMetrics) \
        .filter(HealthMetrics.user_id == user_id) \
        .all()

    if not user_health_metrics_history:
        return {}  # No metrics found for the user

    # Initialize empty lists for each metric
    trend_analysis_report = {
        'heart_rate': {'min': None, 'max': None},
        'blood_pressure': {'min': None, 'max': None},
        'body_temperature': {'min': None, 'max': None},
        'blood_sugar_level': {'min': None, 'max': None},
    }

    # Extract metrics history into separate lists
    for metrics in user_health_metrics_history:
        trend_analysis_report['heart_rate']['min'] = metrics.min_heart_rate
        trend_analysis_report['heart_rate']['max'] = metrics.max_heart_rate
        trend_analysis_report['blood_pressure']['min'] = metrics.min_blood_pressure
        trend_analysis_report['blood_pressure']['max'] = metrics.max_blood_pressure
        trend_analysis_report['body_temperature']['min'] = metrics.min_body_temperature
        trend_analysis_report['body_temperature']['max'] = metrics.max_body_temperature
        trend_analysis_report['blood_sugar_level']['min'] = metrics.min_blood_sugar_level
        trend_analysis_report['blood_sugar_level']['max'] = metrics.max_blood_sugar_level

    return trend_analysis_report