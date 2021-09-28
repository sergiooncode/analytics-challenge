from dataclasses import dataclass


@dataclass
class MetricRecord:
    metric_name: str
    value: int
