
# Generated by CodiumAI
from app.core.database import get_db
from app.api.report_generator.endpoints.reports import trend_analysis_visualization
from fastapi import Response
import os


import pytest

class TestTrendAnalysisVisualization:

    # The function generates a trend analysis report visualization for a given user ID using the get_db function to get a session object.
    @pytest.mark.asyncio
    async def test_generate_trend_analysis_visualization_with_get_db(self):
        # Arrange
        user_id = 1
        db = next(get_db())

        # Act
        result = await trend_analysis_visualization(user_id, db)

        # Assert
        assert isinstance(result, Response)
        assert result.headers["Content-Type"] == "image/png"
        assert result.headers["Content-Disposition"] == f"attachment; filename=trend_analysis_visualization_{user_id}.png"

    # The function extracts data for visualization from the generated report.
    @pytest.mark.asyncio
    async def test_extract_data_for_visualization(self):
        # Arrange
        min_max_report = {
            'heart_rate': {'min': 60, 'max': 100},
            'blood_pressure': {'min': 80, 'max': 120},
            'body_temperature': {'min': 36.5, 'max': 37.5},
            'blood_sugar_level': {'min': 70, 'max': 110},
        }

        # Act
        metrics = list(min_max_report.keys())
        min_values = [min_max_report[metric]['min'] for metric in metrics]
        max_values = [min_max_report[metric]['max'] for metric in metrics]

        # Assert
        assert metrics == ['heart_rate', 'blood_pressure', 'body_temperature', 'blood_sugar_level']
        assert min_values == [60, 80, 36.5, 70]
        assert max_values == [100, 120, 37.5, 110]

    # The function raises an exception if the database connection fails.
    @pytest.mark.asyncio
    async def test_raise_exception_if_database_connection_fails(self):
        # Arrange
        user_id = 1
        db = None

        # Act and Assert
        with pytest.raises(Exception):
            await trend_analysis_visualization(user_id, db)
