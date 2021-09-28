from typing import Dict

from src.metrics.catalogue.domain.exception.metric_with_company_level_and_parent_not_allowed import (
    MetricWithCompanyLevelAndParentNotAllowed,
)
from src.metrics.catalogue.domain.model.metric import Metric, MetricLevelEnum


class RecordMetricCommandTransformer:
    def __init__(self, request_json: Dict[str, str]):
        self.__request_json = request_json

    def transform_request(self) -> Metric:
        if self.__has_company_level_and_parent_metric():
            raise MetricWithCompanyLevelAndParentNotAllowed()

        metric = Metric(
            name=self.__request_json["name"],
            level=MetricLevelEnum.agent.value
            if (self.__request_json["level"]) == MetricLevelEnum.agent.value
            else MetricLevelEnum.company.value,
        )
        if (
            "parent_metric" in self.__request_json
            and self.__request_json["parent_metric"]
        ):
            metric.parent_metric = self.__request_json["parent_metric"]

        return metric

    def __has_company_level_and_parent_metric(self):
        has_company_level_and_parent_metric = (
            self.__request_json["level"] == MetricLevelEnum.company.value
            and "parent_metric" in self.__request_json
            and bool(self.__request_json["parent_metric"])
        )
        return has_company_level_and_parent_metric
