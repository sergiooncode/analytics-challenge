import statistics
from datetime import datetime

from sqlalchemy.sql import func

from src.metrics.aggregation.domain.metric_aggregation_repository import (
    MetricAggregationRepository,
)
from src.metrics.core.persistence.models import Metric
from src.metrics.core.persistence.models.metric_record import MetricRecord


class SqlalchemyMetricAggregationRepository(MetricAggregationRepository):
    def aggregate(
        self, metric_name: str, min_date: datetime, max_date: datetime
    ) -> float:
        given_metric_metric_tree = MetricRecord.query.filter(
            MetricRecord.metric.has(name=metric_name),
            MetricRecord.created_at >= min_date,
            MetricRecord.created_at <= max_date,
        ).all()

        given_metric_children_tree = (
            MetricRecord.query.join(Metric)
            .filter(
                Metric.parent_metric_id.in_(
                    (
                        o.id
                        for o in Metric.query.filter_by(name=metric_name).all()
                        if o is not None
                    )
                ),
                MetricRecord.created_at >= min_date,
                MetricRecord.created_at <= max_date,
            )
            .all()
        )

        given_metric_children_tree_values = [
            o.value for o in given_metric_children_tree
        ]
        given_metric_metric_tree_values = [o.value for o in given_metric_metric_tree]
        given_metric_children_tree_values.extend(given_metric_metric_tree_values)

        return (
            statistics.mean(given_metric_children_tree_values)
            if given_metric_children_tree_values
            else 0
        )
