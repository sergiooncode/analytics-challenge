import json
from datetime import datetime

from src.metrics.catalogue.domain.model.metric import MetricLevelEnum
from src.metrics.core.persistence.models import MetricRecord, Metric


def test_when_are_listed_but_there_are_none(client, session):
    resp = client.get("/metrics/records")

    assert {"data": []} == json.loads(resp.data)


def test_when_are_listed_and_there_is_one(client, session):
    metric_name = "metric_one"
    session.add_all([Metric(name=metric_name, level=MetricLevelEnum.agent.value)])
    session.commit()
    metric_id = session.query(Metric).filter_by(name=metric_name).all()[0].id
    session.add_all(
        [
            MetricRecord(
                metric_id=metric_id,
                value=10,
                created_at=datetime.strptime("2021-09-25", "%Y-%m-%d"),
            )
        ]
    )
    session.commit()

    resp = client.get("/metrics/records")

    assert {
        "data": [
            {
                "metric_name": "metric_one",
                "timestamp": "Sat, 25 Sep 2021 00:00:00 GMT",
                "value": 10,
            }
        ]
    } == json.loads(resp.data)


def test_when_are_listed_in_chronological_order(client, session):
    metric_name = "metric_one"
    session.add_all([Metric(name=metric_name, level=MetricLevelEnum.agent.value)])
    session.commit()
    metric_id = session.query(Metric).filter_by(name=metric_name).all()[0].id
    session.add_all(
        [
            MetricRecord(
                metric_id=metric_id,
                value=10,
                created_at=datetime.strptime("2021-09-25", "%Y-%m-%d"),
            ),
            MetricRecord(
                metric_id=metric_id,
                value=100,
                created_at=datetime.strptime("2021-09-27", "%Y-%m-%d"),
            ),
        ]
    )
    session.commit()

    resp = client.get("/metrics/records")

    assert {
        "data": [
            {
                "metric_name": "metric_one",
                "timestamp": "Mon, 27 Sep 2021 00:00:00 GMT",
                "value": 100,
            },
            {
                "metric_name": "metric_one",
                "timestamp": "Sat, 25 Sep 2021 00:00:00 GMT",
                "value": 10,
            },
        ]
    } == json.loads(resp.data)


def test_when_are_recorded_and_metric_exists(client, session):
    metric_name = "metric_one"
    session.add_all([Metric(name=metric_name, level=MetricLevelEnum.agent.value)])
    session.commit()

    resp = client.post(
        "/metrics/records",
        data=json.dumps(dict(metric_name=metric_name, value=10)),
        content_type="application/json",
    )

    metric_records_recorded = session.query(MetricRecord).all()

    assert 201 == resp.status_code
    assert b"" == resp.data
    assert 1 == len(metric_records_recorded)
    assert metric_name == metric_records_recorded[0].metric.name
    assert 10 == metric_records_recorded[0].value


def test_when_are_recorded_and_metric_doesnt_exist(client, session):
    metric_name = "metric_one"

    resp = client.post(
        "/metrics/records",
        data=json.dumps(dict(metric_name=metric_name, value=10)),
        content_type="application/json",
    )

    metric_records_recorded = session.query(MetricRecord).all()

    assert 422 == resp.status_code
    assert b"" == resp.data
    assert 0 == len(metric_records_recorded)
