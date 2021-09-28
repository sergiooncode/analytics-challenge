class AgentLevelMetricWithAgentLevelParentMetricNotAllowed(Exception):
    def __init__(self):
        super().__init__(
            f"Metric with AGENT level with AGENT parent metric not allowed"
        )
