from matplotlib import pyplot as plt
from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
import os
from app.api.report_generator.generator import generate_overview_report, generate_min_max_report
from app.core.database import get_db
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from fastapi import HTTPException
import logging
from app.models.models import User

router = APIRouter()
logger = logging.getLogger(__name__)
# Define the route to generate the report
@router.get("/{user_id}", dependencies=[Depends(HTTPBearer())])
async def generate_report(user_id: int, db: Session = Depends(get_db), authorize: AuthJWT = Depends()):
    # Check if the user is authorized to access the report
    authorize.jwt_required()
    current_user = authorize.get_jwt_subject()
    raw_jwt = authorize.get_raw_jwt()
    user_email = db.query(User.email).filter(User.user_id == user_id).scalar()
    logger.info("Current user: %s", current_user)
    logger.info("Raw JWT: %s", raw_jwt)
    logger.info("User email: %s", user_email)
    if user_email is None:
        raise HTTPException(status_code=404, detail="User not found") 
    elif current_user != user_email and not raw_jwt.get("isAdmin"):
        raise HTTPException(status_code=401, detail="Not authorized to access this report")

    # Generate the report and return the file response
    overview_report = generate_overview_report(user_id, db)
    min_max_report = generate_min_max_report(user_id, db)

    # Extracting data for the bar chart
    metrics = ['heart_rate', 'blood_pressure', 'body_temperature', 'blood_sugar_level']
    current_values = [float(overview_report.get(metric, 0)) for metric in metrics]
    min_values = [float(min_max_report[metric]['min']) for metric in metrics]
    max_values = [float(min_max_report[metric]['max']) for metric in metrics]

    # Creating the bar chart
    fig, ax = plt.subplots()
    bar_width = 0.3
    index = range(len(metrics))
    opacity = 0.8

    plt.bar(index, current_values, bar_width, alpha=opacity, color='b', label='Current')
    plt.bar([i + bar_width for i in index], max_values, bar_width, alpha=opacity, color='r', label='Max')
    plt.bar([i - bar_width for i in index], min_values, bar_width, alpha=opacity, color='g', label='Min')

    plt.xlabel('Metrics')
    plt.ylabel('Values')
    plt.title('Current vs Min-Max Metrics')
    plt.xticks([i for i in index], metrics)
    plt.legend()

    # Save the plot as a PNG file with the user's ID in the filename
    image_path = f'comparison_chart_{user_id}.png'
    plt.savefig(image_path, format='png')

    # Prepare response to initiate file download
    file_response = Response(content=open(image_path, 'rb').read())
    file_response.headers["Content-Disposition"] = f"attachment; filename={image_path}"
    file_response.headers["Content-Type"] = "image/png"

    # Delete the PNG file after download
    os.remove(image_path)

    return file_response

@router.get("/overview/{user_id}")
async def overview_visualization(user_id: int, db: Session = Depends(get_db)):
    overview_report = generate_overview_report(user_id, db)

    metrics = list(overview_report.keys())
    values = list(overview_report.values())

    # Ensure values are converted to numeric types (float or int)
    try:
        values = [float(value) for value in values]
    except ValueError:
        # Handle the case where a value cannot be converted to float
        return Response(content="Invalid values in overview report", status_code=400)

    plt.figure(figsize=(10, 8))
    plt.bar(metrics, values, color='skyblue')  # Use bar instead of barh
    plt.ylabel('Values')
    plt.title('Overview Report Visualization')
    plt.xticks(rotation=45)  # Rotate x-axis labels for readability

    image_path = f'overview_visualization_{user_id}.png'
    plt.tight_layout()
    plt.savefig(image_path, format='png')

    # Prepare response to initiate file download
    file_response = Response(content=open(image_path, 'rb').read())
    file_response.headers["Content-Disposition"] = f"attachment; filename={image_path}"
    file_response.headers["Content-Type"] = "image/png"

    # Delete the PNG file after download
    os.remove(image_path)

    return file_response


@router.get("/trend_analysis/{user_id}")
async def trend_analysis_visualization(user_id: int, db: Session = Depends(get_db)):
    min_max_report = generate_min_max_report(user_id, db)

    if not min_max_report:
        return Response(content="No data available for trend analysis", media_type="text/plain")

    metrics = list(min_max_report.keys())
    min_values = [min_max_report[metric]['min'] for metric in metrics]
    max_values = [min_max_report[metric]['max'] for metric in metrics]

    plt.figure(figsize=(10, 6))
    plt.plot(metrics, min_values, marker='o', label='Min Values')
    plt.plot(metrics, max_values, marker='x', label='Max Values')
    plt.xlabel('Metrics')
    plt.ylabel('Values')
    plt.title('Trend Analysis Report Visualization')
    plt.legend()

    image_path = f'trend_analysis_visualization_{user_id}.png'
    plt.savefig(image_path, format='png')

    file_response = Response(content=open(image_path, 'rb').read())
    file_response.headers["Content-Disposition"] = f"attachment; filename={image_path}"
    file_response.headers["Content-Type"] = "image/png"

    os.remove(image_path)

    return file_response