from flask import Blueprint

from src.metrics.catalogue.infrastructure.controller import MetricsCatalogueController

METRICS = "/metrics"
METRICS_CATALOGUE = "/catalogue"

# Metrics catalogue, records and aggregation endpoints
metrics_api = Blueprint("metrics_api", __name__, url_prefix=METRICS)
# Catalogue endpoint
metrics_catalogue_api_view = MetricsCatalogueController.as_view(
    "metrics_catalogue_api_view"
)
metrics_api.add_url_rule(
    f"{METRICS_CATALOGUE}",
    view_func=metrics_catalogue_api_view,
    methods=["POST"],
)
