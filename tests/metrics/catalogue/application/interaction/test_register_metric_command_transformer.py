from src.metrics.catalogue.application.interaction.register_metric_command_transformer import (
    RecordMetricCommandTransformer,
)
from src.metrics.catalogue.domain.exception.metric_with_company_level_and_parent_not_allowed import \
    MetricWithCompanyLevelAndParentNotAllowed
from src.metrics.catalogue.domain.model.metric import Metric, MetricLevelEnum


def test_when_a_complete_body_is_received():
    metric_name = "another_metric_8"
    parent_metric_name = "another_metric_5"
    request_body = {
        "name": metric_name,
        "level": MetricLevelEnum.agent.value,
        "parent_metric": parent_metric_name,
    }

    metric_to_register = RecordMetricCommandTransformer(
        request_json=request_body
    ).transform_request()

    assert isinstance(metric_to_register, Metric)
    assert metric_name == metric_to_register.name
    assert parent_metric_name == metric_to_register.parent_metric
    assert MetricLevelEnum.agent.value == metric_to_register.level


def test_when_a_complete_body_is_received_but_is_company_level_and_has_parent_metric():
    metric_name = "another_metric_2"
    parent_metric_name = "another_metric_1"
    request_body = {
        "name": metric_name,
        "level": MetricLevelEnum.company.value,
        "parent_metric": parent_metric_name,
    }

    try:
        RecordMetricCommandTransformer(
            request_json=request_body
        ).transform_request()
    except Exception as exc:
        assert isinstance(exc, MetricWithCompanyLevelAndParentNotAllowed)
