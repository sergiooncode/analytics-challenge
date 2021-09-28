from datetime import datetime

from sqlalchemy.sql import func, case

from src.metrics.aggregation.domain.metric_aggregation_repository import (
    MetricAggregationRepository,
)
from src.metrics.core.persistence.models import session, Metric
from src.metrics.core.persistence.models.metric_record import MetricRecord


class SqlalchemyMetricAggregationRepository(MetricAggregationRepository):
    def aggregate(
        self, metric_name: str, min_date: datetime, max_date: datetime
    ) -> float:
        return session.query(
            func.avg(MetricRecord.value).filter(
                MetricRecord.created_at >= min_date,
                MetricRecord.created_at <= max_date,
            )
        ).all()
