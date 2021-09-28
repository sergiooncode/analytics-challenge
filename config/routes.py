from flask import Blueprint

from src.metrics.catalogue.infrastructure.controller import MetricsCatalogueController
from src.metrics.records.infrastructure.controller import MetricRecordsController

METRICS = "/metrics"
METRICS_CATALOGUE = "/catalogue"
METRICS_RECORDS = "/records"

# Metrics catalogue, records and aggregation endpoints
metrics_api = Blueprint("metrics_api", __name__, url_prefix=METRICS)
# Catalogue endpoint
metrics_catalogue_api_view = MetricsCatalogueController.as_view(
    "metrics_catalogue_api_view"
)
metrics_api.add_url_rule(
    f"{METRICS_CATALOGUE}",
    view_func=metrics_catalogue_api_view,
    methods=["GET", "POST"],
)
metrics_api.add_url_rule(
    f"{METRICS_CATALOGUE}/<string:metric_name>",
    view_func=metrics_catalogue_api_view,
    methods=["GET"],
)
# Metric records endpoint
metric_records_api_view = MetricRecordsController.as_view("metric_records_api_view")
metrics_api.add_url_rule(
    f"{METRICS_RECORDS}",
    view_func=metric_records_api_view,
    methods=["GET", "POST"],
)
