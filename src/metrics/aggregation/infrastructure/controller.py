import traceback

from flask.views import MethodView
from flask import jsonify, make_response, request

from src.metrics.aggregation.application.aggregate_metric_use_case import (
    AggregateMetricUseCase,
)
from src.metrics.aggregation.domain.metric_aggregation_repository import (
    MetricAggregationRepository,
)
from src.metrics.aggregation.infrastructure.persistence.sqlalchemy.sqlalchemy_metric_aggregation_repository import (
    SqlalchemyMetricAggregationRepository,
)


class MetricAggregationController(MethodView):
    def __init__(self):
        metric_aggregation_repository: MetricAggregationRepository = (
            SqlalchemyMetricAggregationRepository()
        )
        self.__aggregate_metric_service = AggregateMetricUseCase(
            metric_aggregation_repository=metric_aggregation_repository
        )

    def post(self, **kwargs):
        aggregation_dict = {}
        try:
            request_body = request.json
            aggregation = self.__aggregate_metric_service.execute(
                metric_name=request_body["metric_name"],
                min_date=request_body["min_date"],
                max_date=request_body["max_date"],
            )
            aggregation_dict = (
                {"data": aggregation} if aggregation is not None else {"data": {}}
            )
        except Exception as exc:
            traceback.print_exc()

        return make_response(jsonify(aggregation_dict))
