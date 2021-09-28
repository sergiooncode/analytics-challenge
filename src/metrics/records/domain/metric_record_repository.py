from abc import ABC, abstractmethod


class MetricRecordRepository(ABC):
    @abstractmethod
    def save(self, metric_name: str, value: int) -> None:
        pass
