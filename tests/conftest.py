import os

import pytest
from alembic.command import upgrade as alembic_upgrade
from alembic.command import downgrade as alembic_downgrade
from alembic.config import Config as AlembicConfig
from sqlalchemy.orm import sessionmaker

from src.app import create_app
from src.metrics.core.persistence.utils import create_db_engine


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


@pytest.fixture(scope="session")
def database(test_app):
    engine = create_db_engine(
        os.environ.get("SQLALCHEMY_DATABASE_URI"), pool_size=10, max_overflow=10 * 2
    )
    session_factory = sessionmaker(bind=engine)

    _db = {
        "engine": engine,
        "session_factory": session_factory,
    }
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    alembic_ini = os.path.join(root_dir, "testing.ini")
    alembic_config = AlembicConfig(alembic_ini)

    alembic_upgrade(alembic_config, "head")

    yield _db

    alembic_downgrade(alembic_config, "base")


@pytest.fixture(scope="function")
def session(database):
    session = database["session_factory"]()

    yield session

    session.rollback()
    session.close()
