from datetime import datetime
from typing import List, Dict, Union

from src.metrics.records.domain.metric_record_repository import MetricRecordRepository


class RetrieveMetricRecordsUseCase:
    def __init__(self, metric_records_repository: MetricRecordRepository):
        self.__metric_records_repository: MetricRecordRepository = (
            metric_records_repository
        )

    def execute(self) -> List[Dict[str, Union[int, str, datetime]]]:
        metric_records = []
        for metric_record_object in self.__metric_records_repository.list():
            metric_record_dict = {
                "name": metric_record_object.metric.name,
                "value": metric_record_object.value,
                "timestamp": metric_record_object.created_at,
            }
            metric_records.append(metric_record_dict)

        return metric_records
