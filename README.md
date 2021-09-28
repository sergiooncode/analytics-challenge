# Metrics API

To start container with docker-compose:
```
make dev
```

## Sending requests to API

### `catalogue` endpoint

- A sample call to register a metric with COMPANY level:

```
curl -v http://localhost/metrics/catalogue -H 'Content-Type: application/json' -d '{"name":"a_company_metric","level":"COMPANY"}'
```
which returns a response with status code 201 CREATED if everything went well

- A sample call to register a metric with AGENT level with a COMPANY level as parent:

```
curl -v http://localhost/metrics/catalogue -H 'Content-Type: application/json' -d '{"name":"an_agent_metric","level":"AGENT", "parent_metric_name":"a_company_metric"}'
```
which returns a response with status code 201 CREATED if everything went well

- A sample call to list all existing metrics:

```
curl -v http://localhost/metrics/catalogue
```

- A sample call to get a specific metric by name:

```
curl -v http://localhost/metrics/catalogue/a_company_metric
```

### `records` endpoint

- A sample call to record a value on a specific metric:

```
curl -v http://localhost/metrics/records -H 'Content-Type: application/json' -d '{"metric_name":"a_company_metric","value":5}'
```
which returns a response with status code 201 CREATED if everything went well

- A sample call to list all metric records in descending chronological order:

```
curl -v http://localhost/metrics/records
```

### `aggregation` endpoint

- A sample call to calculate the average on a given metric:
```
curl -v http://localhost/metrics/aggregation -H 'Content-Type: application/json' -d '{"metric_name":"another_metric_4","min_date":"2021-09-24","max_date":"2021-09-26"}'
```

## To run automated tests

### Unit

To run all tests in the suite:
```
make unit-tests
```

### Integration

Start test container:
```
make test
```

To run all tests in the suite:
```
make integration-tests
```
Or to run a specific test:
```
make custom-integration-tests TEST_PATH=tests/metrics/catalogue/infrastructure/test_controller.py::test_when_metric_created_with_existent_parent
```

## Development

1. Three components have been developed following the corresponding features described in the requirements doc of
the challenge.
2. The above gave place to 3 sub-applications or components part of the `metrics` business domain which are `catalogue`, `records`,
and `aggregation`.
3. Each of those components has 3 layers: domain, application and infrastructure which communicate such that:
domain <> application <> infrastructure
4. The domain layer contains the business logic in its minimal expression. The application


## Considerations

1. Since one of the non-functional requirements is that the components have to be deployed as AWS Lambda functions
the dependencies required for the components (exposed through each of the 3 API endpoints) are kept to a minimum to
minimize the deployment package since that's one of AWS Lambda recommended best practices
(https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html).

2. Regardless the previous consideration since a local environment is still necessary during the development cycle
a Docker-based local environment with all necessary dependencies is considered but having in mind that any
dependency that will end up being deployed in production has to be properly thought out following the
constraint explained in point 1.

## Deployment

### Considerations

1. The package zappa was considered to deploy components as AWS Lambda functions however installing it came
with a fair share of issues like having to pin the version of some zappa dependencies since there have been
deprecations. Also having to downgrade to Python 3.6.x which gave a lot of problems with dependencies other than
zappa.

## Improvements

1. Validate more thoroughly the request body in the requests received by the different endpoints
2. Add more tests for corner cases
3. Add pagination to retrieve action in metric records endpoint

