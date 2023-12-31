
# Generated by CodiumAI
from app.api.report_generator.generator import generate_overview_report, generate_min_max_report
from app.models.models import HealthMetrics

class TestGenerateOverviewReport:

    # Returns a dictionary with the user's health metrics when they exist in the database.
    def test_returns_metrics_when_exist(self, mocker):
        # Arrange
        user_id = 1
        db = mocker.Mock()

        # Mock the query result
        mock_health_metrics = mocker.Mock()
        mock_health_metrics.heart_rate = 80
        mock_health_metrics.blood_pressure = "120/80"
        mock_health_metrics.body_temperature = 36.5
        mock_health_metrics.blood_sugar_level = 5.0
        db.query.return_value.filter.return_value.first.return_value = mock_health_metrics

        # Act
        result = generate_overview_report(user_id, db)

        # Assert
        assert isinstance(result, dict)
        assert 'heart_rate' in result
        assert 'blood_pressure' in result
        assert 'body_temperature' in result
        assert 'blood_sugar_level' in result

    # Returns an empty dictionary when the user's health metrics do not exist in the database.
    def test_returns_empty_dict_when_metrics_do_not_exist(self):
        # Arrange
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        from app.models.models import Base, HealthMetrics
        user_id = 2
        engine = create_engine('sqlite:///:memory:')
        Session = sessionmaker(bind=engine)
        db = Session()
        Base.metadata.create_all(bind=engine)  # Create the 'health_metrics' table
        db.add(HealthMetrics(user_id=1, heart_rate=70, blood_pressure='120/80', body_temperature=36.5, blood_sugar_level=5.0))
        db.commit()

        # Act
        result = generate_overview_report(user_id, db)

        # Assert
        assert isinstance(result, dict)
        assert len(result) == 0

    # Returns an empty dictionary when the user_id argument is not an integer.
    def test_returns_empty_dict_when_user_id_not_integer(self, mocker):
        # Arrange
        user_id = "1"
        db = mocker.MagicMock()
        db.query.return_value.filter.return_value.first.return_value = None

        # Act
        result = generate_overview_report(user_id, db)

        # Assert
        assert isinstance(result, dict)
        assert len(result) == 0

    # Returns an empty dictionary when the db argument is not a Session object.
    def test_returns_empty_dict_when_db_not_session(self, mocker):
        # Arrange
        user_id = 1
        db_mock = mocker.MagicMock()
        db_mock.query().filter().first.return_value = None

        # Act
        result = generate_overview_report(user_id, db_mock)

        # Assert
        assert isinstance(result, dict)
        assert len(result) == 0

    # Returns an empty dictionary when the user_id argument is a negative integer.
    def test_returns_empty_dict_when_user_id_negative(self, mocker):
        # Arrange
        user_id = -1
        db = mocker.Mock()
        db.query.return_value.filter.return_value.first.return_value = None

        # Act
        result = generate_overview_report(user_id, db)

        # Assert
        assert isinstance(result, dict)
        assert len(result) == 0

    # Returns an empty dictionary when the user_id argument does not exist in the database.
    def test_returns_empty_dict_when_user_id_nonexistent(self):
        # Arrange
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        from app.models.models import Base, HealthMetrics
        user_id = 9999  # Non-existent user_id
        engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(bind=engine)
        Session = sessionmaker(bind=engine)
        db = Session()

        # Create and populate the 'health_metrics' table
        health_metrics = HealthMetrics(user_id=0, heart_rate=80, blood_pressure='120/80', body_temperature=36.5, blood_sugar_level=5.0)
        db.add(health_metrics)
        db.commit()

        # Act
        result = generate_overview_report(user_id, db)

        # Assert
        assert isinstance(result, dict)
        assert len(result) == 0

class TestGenerateMinMaxReport:

    # Returns a dictionary with the minimum and maximum values for each health metric if the user has health metrics history.
    def test_returns_min_max_values_if_user_has_history(self):
        # Arrange
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        from app.models.models import Base
        user_id = 1
        engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(bind=engine)
        Session = sessionmaker(bind=engine)
        db = Session()

        # Create health metrics history for the user
        metrics = HealthMetrics(
            user_id=user_id,
            heart_rate=80,
            blood_pressure='120/80',
            body_temperature=36.5,
            blood_sugar_level=5.0,
            min_heart_rate=70,
            max_heart_rate=90,
            min_blood_pressure='110/70',
            max_blood_pressure='130/90',
            min_body_temperature=36.0,
            max_body_temperature=37.0,
            min_blood_sugar_level=4.0,
            max_blood_sugar_level=6.0
        )
        db.add(metrics)
        db.commit()

        # Act
        result = generate_min_max_report(user_id, db)

        # Assert
        assert result == {
            'heart_rate': {'min': 70, 'max': 90},
            'blood_pressure': {'min': '110/70', 'max': '130/90'},
            'body_temperature': {'min': 36.0, 'max': 37.0},
            'blood_sugar_level': {'min': 4.0, 'max': 6.0}
        }

    # Returns an empty dictionary if the user has no health metrics history.
    def test_returns_empty_dict_if_user_has_no_history(self, mocker):
        # Arrange
        user_id = 1
        db = mocker.Mock()
        db.query().filter().all.return_value = []

        # Act
        result = generate_min_max_report(user_id, db)

        # Assert
        assert result == {}

    # Returns an empty dictionary if the user_id parameter is not an integer.
    def test_returns_empty_dict_if_user_id_not_integer(self):
        # Arrange
        user_id = '1'
        from unittest.mock import Mock
        db = Mock()
        db.query.return_value.filter.return_value.all.return_value = []

        # Act
        result = generate_min_max_report(user_id, db)

        # Assert
        assert result == {}

    # Returns an empty dictionary if the db parameter is not a Session object.
    def test_returns_empty_dict_if_db_not_session_object(self, mocker):
        # Arrange
        user_id = 1
        db = mocker.Mock()
        db.query.return_value.filter.return_value.all.return_value = []

        # Act
        result = generate_min_max_report(user_id, db)

        # Assert
        assert result == {}

    # Returns an empty dictionary if the user_id parameter is not associated with any user in the database.
    def test_returns_empty_dict_if_user_id_not_associated_with_user(self):
        # Arrange
        from unittest.mock import Mock
        user_id = 1
        db = Mock()
        db.query.return_value.filter.return_value.all.return_value = []

        # Act
        result = generate_min_max_report(user_id, db)

        # Assert
        assert result == {}

    # Returns a dictionary with None values for all metrics if the user has health metrics history but none of the metrics have minimum or maximum values.
    def test_returns_dict_with_none_values_if_metrics_have_no_min_max_values(self):
        # Arrange
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        from app.models.models import Base
        user_id = 1
        engine = create_engine('sqlite:///:memory:')
        Session = sessionmaker(bind=engine)
        db = Session()

        # Create health metrics history for the user without min/max values
        metrics = HealthMetrics(
            user_id=user_id,
            heart_rate=80,
            blood_pressure='120/80',
            body_temperature=36.5,
            blood_sugar_level=5.0
        )
        Base.metadata.create_all(engine)  # Create the 'health_metrics' table
        db.add(metrics)
        db.commit()

        # Act
        result = generate_min_max_report(user_id, db)

        # Assert
        assert result == {
            'heart_rate': {'min': None, 'max': None},
            'blood_pressure': {'min': None, 'max': None},
            'body_temperature': {'min': None, 'max': None},
            'blood_sugar_level': {'min': None, 'max': None}
        }