from datetime import datetime

from src.metrics.aggregation.domain.metric_aggregation_repository import (
    MetricAggregationRepository,
)
from src.metrics.core.persistence.models.metric_record import MetricRecord


class SqlalchemyMetricAggregationRepository(MetricAggregationRepository):
    def aggregate(
        self, metric_name: str, min_date: datetime, max_date: datetime
    ) -> float:
        children_metrics_value_sum = 0
        number_of_metrics_to_average = 1
        metric_value = 0.0
        metric_tree = (
            MetricRecord.query
            .filter(
                MetricRecord.metric.has(name=metric_name),
                MetricRecord.created_at >= min_date,
                MetricRecord.created_at <= max_date,
            )
            .all()
        )
        if metric_tree:
            metric_value = metric_tree[0].value
            children_metrics_dict = metric_tree[0].metric.children_metrics
            children_metrics_ids = (
                children_metrics_dict[children_metric_name].id
                for children_metric_name in children_metrics_dict
            )
            children_metric_records = MetricRecord.query.filter(MetricRecord.metric_id.in_(children_metrics_ids)).all()
            for children_metric_record in children_metric_records:
                children_metrics_value_sum += children_metric_record.value
            if children_metrics_value_sum != 0:
                number_of_metrics_to_average += len(children_metric_records)
        return (
            metric_value + children_metrics_value_sum
        ) / number_of_metrics_to_average
