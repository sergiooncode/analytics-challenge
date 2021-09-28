import json

from src.metrics.catalogue.domain.model.metric import MetricLevelEnum
from src.metrics.core.persistence.models import Metric


def test_when_are_listed_but_there_are_none(client, session):
    resp = client.get("/metrics/catalogue")

    assert {"data": []} == json.loads(resp.data)


def test_when_are_listed_and_there_is_one(client, session):
    metric_name = "metric_one"
    session.add_all([Metric(name=metric_name, level=MetricLevelEnum.agent.value)])
    session.commit()

    resp = client.get("/metrics/catalogue")

    assert {
        "data": [{"level": MetricLevelEnum.agent.value, "name": metric_name}]
    } == json.loads(resp.data)


def test_when_metric_created_with_existent_parent(client, session):
    metric_name = "metric_two"
    parent_metric_name = "a_parent_metric"
    session.add_all(
        [Metric(name=parent_metric_name, level=MetricLevelEnum.company.value)]
    )
    session.commit()
    resp = client.post(
        "/metrics/catalogue",
        data=json.dumps(
            dict(
                name=metric_name,
                level="AGENT",
                parent_metric=parent_metric_name,
            )
        ),
        content_type="application/json",
    )

    metrics_created = session.query(Metric).all()

    assert 201 == resp.status_code
    assert b"" == resp.data
    assert 2 == len(metrics_created)
    for mc in metrics_created:
        assert mc.name in [metric_name, parent_metric_name]
        assert mc.level in [MetricLevelEnum.company.value, MetricLevelEnum.agent.value]


def test_when_metric_tried_to_be_created_with_non_existent_parent(client, session):
    metric_name = "a_metric"
    parent_metric_name = "another_parent_metric"
    resp = client.post(
        "/metrics/catalogue",
        data=json.dumps(
            dict(
                name=metric_name,
                level="AGENT",
                parent_metric=parent_metric_name,
            )
        ),
        content_type="application/json",
    )

    metrics_created = session.query(Metric).all()

    assert 422 == resp.status_code
    assert {
        "message": f"Parent metric {parent_metric_name} doesnt exist"
    } == json.loads(resp.data)
    assert 0 == len(metrics_created)
