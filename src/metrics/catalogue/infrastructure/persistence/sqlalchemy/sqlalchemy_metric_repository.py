from sqlalchemy.exc import DatabaseError, IntegrityError

from src.metrics.catalogue.domain.exception.same_name_metric_exists import (
    SameNameMetricExists,
)
from src.metrics.catalogue.domain.metric_repository import MetricRepository
from src.metrics.catalogue.domain.model.metric import Metric as MetricModel
from src.metrics.core.persistence.models import session
from src.metrics.core.persistence.models.metric import Metric


class SqlalchemyMetricRepository(MetricRepository):
    def save(self, metric: MetricModel, parent_metric_id: int) -> None:
        try:
            metric_object = Metric(name=metric.name, level=metric.level)
            if metric.parent_metric:
                metric_object.parent_metric = parent_metric_id
            session.add_all([metric_object])
            session.commit()
        except IntegrityError:
            session.rollback()
            raise SameNameMetricExists(metric.name)
        except DatabaseError:
            session.rollback()

        return None
