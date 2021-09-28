from abc import abstractmethod, ABC

from src.metrics.catalogue.domain.model.metric import Metric as MetricModel


class MetricRepository(ABC):
    @abstractmethod
    def save(self, metric: MetricModel) -> None:
        pass
