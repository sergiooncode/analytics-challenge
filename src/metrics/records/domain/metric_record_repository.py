from abc import ABC, abstractmethod
from typing import List

from src.metrics.core.persistence.models.metric_record import MetricRecord


class MetricRecordRepository(ABC):
    @abstractmethod
    def list(self) -> List[MetricRecord]:
        pass

    @abstractmethod
    def save(self, metric_name: str, value: int) -> None:
        pass
