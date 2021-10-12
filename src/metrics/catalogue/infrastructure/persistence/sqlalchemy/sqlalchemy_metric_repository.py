from typing import List

from sqlalchemy.exc import DatabaseError, IntegrityError

from src.metrics.catalogue.domain.exception.same_name_metric_exists import (
    SameNameMetricExists,
)
from src.metrics.catalogue.domain.metric_repository import MetricRepository
from src.metrics.catalogue.domain.model.metric import Metric as MetricModel
from src.metrics.core.persistence.models import db
from src.metrics.core.persistence.models.metric import Metric


class SqlalchemyMetricRepository(MetricRepository):
    def list(self, name: str = None) -> List[Metric]:
        q = Metric.query
        if name:
            q = q.filter_by(name=name)
        return q.all()

    def save(self, metric: MetricModel, parent_metric_id: int) -> None:
        try:
            metric_object = Metric(name=metric.name, level=metric.level)
            db.session.add_all([metric_object])
            db.session.commit()
            if parent_metric_id:
                metric_object.parent_metric_id = parent_metric_id
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise SameNameMetricExists(metric.name)
        except DatabaseError:
            db.session.rollback()

        return None
