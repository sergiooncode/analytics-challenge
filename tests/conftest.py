import os
from datetime import datetime

import pytest
from alembic.command import downgrade as alembic_downgrade
from alembic.command import upgrade as alembic_upgrade
from alembic.config import Config as AlembicConfig
from sqlalchemy.orm.session import close_all_sessions

from src.app import create_app
from src.metrics.catalogue.domain.model.metric import MetricLevelEnum
from src.metrics.core.persistence.models import Metric, MetricRecord
from src.metrics.core.persistence.models import db


@pytest.fixture(scope="session")
def test_app():
    app = create_app(config_name="test")

    context = app.app_context()
    context.push()

    yield app

    context.pop()


@pytest.fixture
def client(test_app):
    with test_app.test_client() as client:
        yield client


@pytest.fixture
def database_setup(test_app):
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    alembic_ini = os.path.join(root_dir, "testing.ini")
    alembic_config = AlembicConfig(alembic_ini)

    db.app = test_app
    alembic_upgrade(alembic_config, "head")

    yield db

    alembic_downgrade(alembic_config, "base")


@pytest.fixture
def session(database_setup, request):
    connection = database_setup.engine.connect()
    transaction = connection.begin()

    from sqlalchemy.orm import scoped_session
    from sqlalchemy.orm import sessionmaker

    session_factory = sessionmaker(bind=database_setup.engine)
    db_session = scoped_session(session_factory)
    database_setup.session = db_session

    def teardown():
        transaction.rollback()
        connection.close()
        db_session.remove()
        close_all_sessions()

    request.addfinalizer(teardown)
    return db_session


@pytest.fixture
def add_agent_level_metric_with_no_records(session):
    metric_name = "metric_one"
    session.add_all([Metric(name=metric_name, level=MetricLevelEnum.agent.value)])
    session.commit()


@pytest.fixture
def add_agent_level_metric_with_one_record(session):
    metric_name = "metric_two"
    session.add_all([Metric(name=metric_name, level=MetricLevelEnum.agent.value)])
    session.commit()
    metric_id = session.query(Metric).filter_by(name=metric_name).all()[0].id
    session.add_all(
        [
            MetricRecord(
                metric_id=metric_id,
                value=10,
                created_at=datetime.strptime("2021-09-25", "%Y-%m-%d"),
            )
        ]
    )
    session.commit()


@pytest.fixture
def add_agent_level_metric_and_two_records(session):
    metric_name = "metric_three"
    session.add_all([Metric(name=metric_name, level=MetricLevelEnum.agent.value)])
    session.commit()
    metric_id = session.query(Metric).filter_by(name=metric_name).all()[0].id
    session.add_all(
        [
            MetricRecord(
                metric_id=metric_id,
                value=10,
                created_at=datetime.strptime("2021-09-25", "%Y-%m-%d"),
            ),
            MetricRecord(
                metric_id=metric_id,
                value=100,
                created_at=datetime.strptime("2021-09-27", "%Y-%m-%d"),
            ),
        ]
    )
    session.commit()
