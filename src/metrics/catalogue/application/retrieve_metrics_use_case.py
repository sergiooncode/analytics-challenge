from typing import Dict, List, Union

from src.metrics.catalogue.domain.metric_repository import MetricRepository


class RetrieveMetricsUseCase:
    def __init__(self, metric_repository: MetricRepository):
        self.__metric_repository: MetricRepository = metric_repository

    def execute(self, metric_name: str = None) -> List[Dict[str, Union[int, str]]]:
        metrics = []
        if metric_name:
            metric_objects = self.__metric_repository.list(name=metric_name)
        else:
            metric_objects = self.__metric_repository.list()

        for metric_object in metric_objects:
            metric_dict = {
                "name": metric_object.name,
                "level": metric_object.level,
            }
            if metric_object.parent_metric_id:
                metric_dict["parent_metric_name"] = metric_object.parent_metric.name
            metrics.append(metric_dict)

        return metrics
