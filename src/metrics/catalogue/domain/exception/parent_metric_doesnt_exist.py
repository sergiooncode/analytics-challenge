class ParentMetricDoesntExist(Exception):
    def __init__(self, metric_name: str):
        self.metric_name = metric_name
        super().__init__(f"Parent metric {self.metric_name} doesnt exist")
