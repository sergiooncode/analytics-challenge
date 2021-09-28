import enum
from dataclasses import dataclass
from typing import Optional


class MetricLevelEnum(enum.Enum):
    agent = "AGENT"
    company = "COMPANY"


@dataclass
class Metric:
    name: str
    level: str
    parent_metric: Optional[str] = None

    def __repr__(self):
        return (
            f"<Metric(name={self.name}, level={self.level},"
            f"parent_metric={self.parent_metric})>"
        )
