from abc import abstractmethod, ABC
from typing import List

from src.metrics.core.persistence.models.metric import Metric
from src.metrics.catalogue.domain.model.metric import Metric as MetricModel


class MetricRepository(ABC):
    @abstractmethod
    def list(self, name: str = None) -> List[Metric]:
        pass

    @abstractmethod
    def save(self, metric: MetricModel) -> None:
        pass
