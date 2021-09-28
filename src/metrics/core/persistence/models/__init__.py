import os

from src.metrics.core.persistence.models.metric import Metric
from src.metrics.core.persistence.models.metric_record import MetricRecord
from src.metrics.core.persistence.utils import create_db_session, create_db_engine

engine = create_db_engine(os.environ.get("SQLALCHEMY_DATABASE_URI"))
session = create_db_session(engine)
