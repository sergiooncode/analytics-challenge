import os

from src.metrics.core.persistence.utils import create_db_session, create_db_engine

engine = create_db_engine(os.environ.get("SQLALCHEMY_DATABASE_URI"))
db = create_db_session()

from src.metrics.core.persistence.models.metric import Metric # noqa
from src.metrics.core.persistence.models.metric_record import MetricRecord # noqa
