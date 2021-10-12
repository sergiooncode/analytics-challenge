from typing import List

from sqlalchemy.exc import DatabaseError

from src.metrics.core.persistence.models import db
from src.metrics.core.persistence.models.metric import Metric
from src.metrics.core.persistence.models.metric_record import MetricRecord
from src.metrics.records.domain.exception.metric_to_record_doesn_exist import (
    MetricToRecordDoesntExist,
)
from src.metrics.records.domain.metric_record_repository import MetricRecordRepository


class SqlalchemyMetricRecordRepository(MetricRecordRepository):
    def list(self) -> List[MetricRecord]:
        return (
            MetricRecord.query.order_by(MetricRecord.created_at.desc()).all()
        )

    def save(self, metric_name: str, value: int) -> None:
        try:
            metric = Metric.query.filter_by(name=metric_name).all()
            if not metric:
                raise MetricToRecordDoesntExist(metric_name)
            db.session.add_all([MetricRecord(value=value, metric_id=metric[0].id)])
            db.session.commit()
        except MetricToRecordDoesntExist as exc:
            raise exc
        except DatabaseError:
            db.session.rollback()

        return None
