import json
import traceback
from typing import Dict, Union, List

from flask import Response
from flask import jsonify, make_response, request
from flask.views import MethodView

from src.metrics.catalogue.application.interaction.register_metric_command_transformer import (
    RecordMetricCommandTransformer,
)
from src.metrics.catalogue.application.register_metric_use_case import (
    RegisterMetricsUseCase,
)
from src.metrics.catalogue.application.retrieve_metrics_use_case import (
    RetrieveMetricsUseCase,
)
from src.metrics.catalogue.domain.exception.agent_level_metric_with_agent_level_parent_metric_not_allowed import (
    AgentLevelMetricWithAgentLevelParentMetricNotAllowed,
)
from src.metrics.catalogue.domain.exception.metric_with_company_level_and_parent_not_allowed import (
    MetricWithCompanyLevelAndParentNotAllowed,
)
from src.metrics.catalogue.domain.exception.parent_metric_doesnt_exist import (
    ParentMetricDoesntExist,
)
from src.metrics.catalogue.domain.exception.same_name_metric_exists import (
    SameNameMetricExists,
)
from src.metrics.catalogue.domain.metric_repository import MetricRepository
from src.metrics.catalogue.infrastructure.persistence.sqlalchemy.sqlalchemy_metric_repository import (
    SqlalchemyMetricRepository,
)


class MetricsCatalogueController(MethodView):
    def __init__(self):
        metric_repository: MetricRepository = SqlalchemyMetricRepository()
        self.__retrieve_metrics_service = RetrieveMetricsUseCase(
            metric_repository=metric_repository
        )
        self.__register_metric_service = RegisterMetricsUseCase(
            metric_repository=metric_repository
        )

    def get(self, **kwargs):
        metrics_dict = {}
        try:
            if "metric_name" in kwargs:
                metrics: List[
                    Dict[str, Union[int, str]]
                ] = self.__retrieve_metrics_service.execute(kwargs["metric_name"])
            else:
                metrics: List[
                    Dict[str, Union[int, str]]
                ] = self.__retrieve_metrics_service.execute()
            metrics_dict = {"data": metrics}
        except Exception:
            traceback.print_exc()

        return make_response(jsonify(metrics_dict))

    def post(self, **kwargs):
        try:
            metric_to_register = RecordMetricCommandTransformer(
                request_json=request.json
            ).transform_request()
            self.__register_metric_service.execute(metric=metric_to_register)
        except MetricWithCompanyLevelAndParentNotAllowed as exc:
            return Response(
                response=json.dumps({"message": str(exc)}),
                status=400,
                content_type="application/json",
            )
        except AgentLevelMetricWithAgentLevelParentMetricNotAllowed as exc:
            return Response(
                response=json.dumps({"message": str(exc)}),
                status=422,
                content_type="application/json",
            )
        except SameNameMetricExists as exc:
            return Response(
                response=json.dumps({"message": str(exc)}),
                status=422,
                content_type="application/json",
            )
        except ParentMetricDoesntExist as exc:
            return Response(
                response=json.dumps({"message": str(exc)}),
                status=422,
                content_type="application/json",
            )
        except Exception:
            traceback.print_exc()

        return Response(status=201)
