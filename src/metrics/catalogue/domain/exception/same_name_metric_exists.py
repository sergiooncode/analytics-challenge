class SameNameMetricExists(Exception):
    def __init__(self, metric_name: str):
        self.metric_name = metric_name
        super().__init__(f"Metric with name {self.metric_name} already exists")
