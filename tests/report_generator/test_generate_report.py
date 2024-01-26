
# Generated by CodiumAI
from app.core.database import get_db
from app.api.report_generator.generator import generate_overview_report
from pytest import Session
from fastapi import HTTPException
from app.api.report_generator.endpoints.reports import generate_report


import pytest

class TestGenerateReport:

    # Generates an overview report for the user's health metrics with proper session setup
    @pytest.mark.asyncio
    async def test_generate_overview_report_with_proper_session_setup(self):
        # Arrange
        user_id = 1
        db = next(get_db())

        # Act
        overview_report = generate_overview_report(user_id, db)

        # Assert
        assert isinstance(overview_report, dict)
        assert 'heart_rate' in overview_report
        assert 'blood_pressure' in overview_report
        assert 'body_temperature' in overview_report
        assert 'blood_sugar_level' in overview_report

    # User is not authorized to access the report
    @pytest.mark.asyncio
    async def test_user_not_authorized(self, mocker):
        # Arrange
        user_id = 2
        db = mocker.Mock()

        # Mock the authorize object and its jwt_required method
        authorize_mock = mocker.Mock()
        authorize_mock.jwt_required.side_effect = HTTPException(status_code=401, detail="Not authorized to access this report")

        # Act and Assert
        with pytest.raises(HTTPException) as exc_info:
            await generate_report(user_id, db, authorize=authorize_mock)
    
        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "Not authorized to access this report"

    # Generates a min-max report for the user's health metrics
    @pytest.mark.asyncio
    async def test_generate_report_with_proper_session_setup(self, mocker):
        # Arrange
        user_id = 1
        db = next(get_db())
        authorize_mock = mocker.Mock()
        authorize_mock.jwt_required.return_value = None

        # Act
        response = await generate_report(user_id, db, authorize=authorize_mock)

        # Assert
        assert response.status_code == 200
        assert response.headers["Content-Disposition"] == f"attachment; filename=comparison_chart_{user_id}.png"
        assert response.headers["Content-Type"] == "image/png"

    # User ID is not found in the database
    @pytest.mark.asyncio
    async def test_user_id_not_found(self, mocker):
        # Arrange
        user_id = 1
        db = next(get_db())
        authorize_mock = mocker.Mock()
        authorize_mock.jwt_required.side_effect = HTTPException(status_code=401, detail="Not authorized to access this report")

        # Act
        with pytest.raises(HTTPException) as exc_info:
            await generate_report(user_id, db, authorize=authorize_mock)

        # Assert
        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "Not authorized to access this report"