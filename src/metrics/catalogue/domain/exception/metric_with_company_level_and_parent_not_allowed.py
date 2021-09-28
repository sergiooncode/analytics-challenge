class MetricWithCompanyLevelAndParentNotAllowed(Exception):
    def __init__(self):
        super().__init__(f"Metric with COMPANY level and parent metric not allowed")
