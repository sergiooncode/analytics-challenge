import traceback
from typing import List, Dict, Union

from flask.views import MethodView
from flask import jsonify, make_response, request
from flask import Response

from src.metrics.records.application.record_metric_record_use_case import (
    RecordMetricRecordsUseCase,
)
from src.metrics.records.application.retrieve_metric_records_use_case import (
    RetrieveMetricRecordsUseCase,
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
        self.__retrieve_metric_records_service = RetrieveMetricRecordsUseCase(
            metric_records_repository=metric_records_repository
        )
        self.__record_metric_record_service = RecordMetricRecordsUseCase(
            metric_records_repository=metric_records_repository
        )

    def get(self, **kwargs):
        metric_records_dict = {}
        try:
            metric_records: List[
                Dict[str, Union[int, str]]
            ] = self.__retrieve_metric_records_service.execute()
            metric_records_dict = {"data": metric_records}
        except Exception as exc:
            traceback.print_exc()

        return make_response(jsonify(metric_records_dict))

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
