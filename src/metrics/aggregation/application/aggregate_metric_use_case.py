from datetime import datetime
from typing import Union, Dict, List

from src.metrics.aggregation.domain.metric_aggregation_repository import (
    MetricAggregationRepository,
)


class AggregateMetricUseCase:
    def __init__(self, metric_aggregation_repository: MetricAggregationRepository):
        self.__metric_aggregation_repository: MetricAggregationRepository = (
            metric_aggregation_repository
        )

    def execute(
        self, metric_name: str, min_date: datetime, max_date: datetime
    ) -> List[Dict[str, Union[float, str]]]:
        aggregation = self.__metric_aggregation_repository.aggregate(
            metric_name=metric_name,
            min_date=min_date,
            max_date=max_date,
        )

        if aggregation[0][0] is not None:
            return {"metric_name": metric_name, "aggregation": float(aggregation[0][0])}
        return None
