from typing import List

from sqlalchemy.exc import DatabaseError

from src.metrics.core.persistence.models import session
from src.metrics.core.persistence.models.metric import Metric
from src.metrics.core.persistence.models.metric_record import MetricRecord
from src.metrics.records.domain.metric_record_repository import MetricRecordRepository


class SqlalchemyMetricRecordRepository(MetricRecordRepository):
    def list(self) -> List[MetricRecord]:
        return (
            session.query(MetricRecord).order_by(MetricRecord.created_at.desc()).all()
        )

    def save(self, metric_name: str, value: int) -> None:
        try:
            metric = session.query(Metric).filter_by(name=metric_name).all()
            session.add_all([MetricRecord(value=value, metric_id=metric[0].id)])
            session.commit()
        except DatabaseError:
            session.rollback()

        return None
