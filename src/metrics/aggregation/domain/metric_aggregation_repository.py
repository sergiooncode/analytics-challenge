from abc import ABC, abstractmethod


class MetricAggregationRepository(ABC):
    @abstractmethod
    def aggregate(self, metric_name: str) -> float:
        pass
