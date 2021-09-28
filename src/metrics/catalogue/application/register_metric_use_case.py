from typing import Dict, List, Union

from src.metrics.catalogue.domain.exception.agent_level_metric_with_agent_level_parent_metric_not_allowed import (
    AgentLevelMetricWithAgentLevelParentMetricNotAllowed,
)
from src.metrics.catalogue.domain.exception.parent_metric_doesnt_exist import (
    ParentMetricDoesntExist,
)
from src.metrics.catalogue.domain.metric_repository import MetricRepository
from src.metrics.catalogue.domain.model.metric import Metric, MetricLevelEnum


class RegisterMetricsUseCase:
    def __init__(self, metric_repository: MetricRepository):
        self.__metric_repository: MetricRepository = metric_repository

    def execute(self, metric: Metric) -> List[Dict[str, Union[int, str]]]:
        parent_metric = []
        parent_metric_id = None
        if metric.parent_metric is not None:
            parent_metric = self.__metric_repository.list(name=metric.parent_metric)
            if not parent_metric:
                raise ParentMetricDoesntExist(metric_name=metric.parent_metric)
            if (
                parent_metric[0].level == MetricLevelEnum.agent.value
                and metric.level == MetricLevelEnum.agent.value
            ):
                raise AgentLevelMetricWithAgentLevelParentMetricNotAllowed()

        if parent_metric:
            parent_metric_id = parent_metric[0].id

        self.__metric_repository.save(metric=metric, parent_metric_id=parent_metric_id)
