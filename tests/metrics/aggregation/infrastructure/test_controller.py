import json
from datetime import datetime

from src.metrics.catalogue.domain.model.metric import MetricLevelEnum
from src.metrics.core.persistence.models import Metric, MetricRecord


def test_when_records_are_aggregated_but_there_are_no_records(client, session):
    metric_name = "a_metric"
    resp = client.post(
        "/metrics/aggregation",
        data=json.dumps(
            dict(
                metric_name=metric_name,
                min_date="2021-09-24",
                max_date="2021-09-26",
            )
        ),
        content_type="application/json",
    )

    assert {"data": {}} == json.loads(resp.data)


def test_when_records_are_aggregated_and_there_are_records_of_agent_metrics(
    client, session
):
    metric_name = "a_metric"
    session.add_all([Metric(name=metric_name, level=MetricLevelEnum.agent.value)])
    session.commit()
    metric_id = session.query(Metric).filter_by(name=metric_name).all()[0].id

    value = 10
    session.add_all(
        [
            MetricRecord(
                value=value,
                metric_id=metric_id,
                created_at=datetime.strptime("2021-09-25", "%Y-%m-%d"),
            )
        ]
    )
    session.commit()

    resp = client.post(
        "/metrics/aggregation",
        data=json.dumps(
            dict(
                metric_name=metric_name,
                min_date="2021-09-24",
                max_date="2021-09-26",
            )
        ),
        content_type="application/json",
    )

    assert {"data": {"aggregation": 10.0, "metric_name": "a_metric"}} == json.loads(
        resp.data
    )


def test_when_records_are_aggregated_and_there_are_records_of_agent_metrics(
    client, session
):
    metric_name = "a_metric"
    session.add_all([Metric(name=metric_name, level=MetricLevelEnum.agent.value)])
    session.commit()
    metric_id = session.query(Metric).filter_by(name=metric_name).all()[0].id

    value = 10
    session.add_all(
        [
            MetricRecord(
                value=value,
                metric_id=metric_id,
                created_at=datetime.strptime("2021-09-25", "%Y-%m-%d"),
            )
        ]
    )
    session.commit()

    resp = client.post(
        "/metrics/aggregation",
        data=json.dumps(
            dict(
                metric_name=metric_name,
                min_date="2021-09-24",
                max_date="2021-09-26",
            )
        ),
        content_type="application/json",
    )

    assert {"data": {"aggregation": 10.0, "metric_name": "a_metric"}} == json.loads(
        resp.data
    )


def test_when_records_are_aggregated_and_there_are_records_of_company_metrics(
    client, session
):
    company_metric_name = "a_company_metric"
    agent_metric_name = "an_agent_metric"
    another_agent_metric_name = "another_agent_metric"
    session.add_all(
        [
            Metric(name=company_metric_name, level=MetricLevelEnum.company.value),
        ]
    )
    company_metric_id = (
        session.query(Metric).filter_by(name=company_metric_name).all()[0].id
    )
    session.add_all(
        [
            Metric(
                name=agent_metric_name,
                level=MetricLevelEnum.agent.value,
                parent_metric_id=company_metric_id,
            )
        ]
    )
    agent_metric_id = (
        session.query(Metric).filter_by(name=agent_metric_name).all()[0].id
    )
    session.add_all(
        [Metric(name=another_agent_metric_name, level=MetricLevelEnum.agent.value)]
    )
    another_agent_metric_id = (
        session.query(Metric).filter_by(name=another_agent_metric_name).all()[0].id
    )

    company_metric_value = 10
    agent_metric_value = 15
    another_agent_metric_value = 20
    session.add_all(
        [
            MetricRecord(
                value=company_metric_value,
                metric_id=company_metric_id,
                created_at=datetime.strptime("2021-09-25", "%Y-%m-%d"),
            ),
            MetricRecord(
                value=agent_metric_value,
                metric_id=agent_metric_id,
                created_at=datetime.strptime("2021-09-25", "%Y-%m-%d"),
            ),
            MetricRecord(
                value=another_agent_metric_value,
                metric_id=another_agent_metric_id,
                created_at=datetime.strptime("2021-09-25", "%Y-%m-%d"),
            ),
        ]
    )
    session.commit()

    resp = client.post(
        "/metrics/aggregation",
        data=json.dumps(
            dict(
                metric_name=company_metric_name,
                min_date="2021-09-24",
                max_date="2021-09-26",
            )
        ),
        content_type="application/json",
    )

    assert {
        "data": {"aggregation": 12.5, "metric_name": "a_company_metric"}
    } == json.loads(resp.data)
