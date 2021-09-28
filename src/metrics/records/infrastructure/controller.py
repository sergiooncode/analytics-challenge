import traceback

from flask import Response
from flask import request
from flask.views import MethodView

from src.metrics.records.application.record_metric_record_use_case import (
    RecordMetricRecordsUseCase,
)
from src.metrics.records.domain.metric_record_repository import MetricRecordRepository
from src.metrics.records.domain.model.metric_record import MetricRecord
from src.metrics.records.infrastructure.persistence.sqlalchemy.sqlalchemy_metric_record_repository import (
    SqlalchemyMetricRecordRepository,
)


class MetricRecordsController(MethodView):
    def __init__(self):
        metric_records_repository: MetricRecordRepository = (
            SqlalchemyMetricRecordRepository()
        )
        self.__record_metric_record_service = RecordMetricRecordsUseCase(
            metric_records_repository=metric_records_repository
        )

    def post(self, **kwargs):
        try:
            request_body = request.json
            metric_record = MetricRecord(
                metric_name=request_body["metric_name"], value=request_body["value"]
            )
            self.__record_metric_record_service.execute(metric_record=metric_record)
        except Exception as exc:
            traceback.print_exc()

        return Response(status=201)
