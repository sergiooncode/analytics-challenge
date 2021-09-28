from src.metrics.records.domain.metric_record_repository import MetricRecordRepository
from src.metrics.records.domain.model.metric_record import MetricRecord


class RecordMetricRecordsUseCase:
    def __init__(self, metric_records_repository: MetricRecordRepository):
        self.__metric_records_repository: MetricRecordRepository = (
            metric_records_repository
        )

    def execute(self, metric_record: MetricRecord) -> None:
        self.__metric_records_repository.save(
            metric_name=metric_record.metric_name, value=metric_record.value
        )
