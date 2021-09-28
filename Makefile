.PHONY: tests

dev:
	docker-compose -f docker-compose.yml up --build

test:
	docker-compose -f docker-compose.test.yml up --build

destroy:
	docker-compose -f docker-compose.yml down

unit-tests:
	docker-compose -f docker-compose.test.yml run -e FLASK_ENV=test -e ENVIRONMENT=test --rm metrics-api pytest -vvv tests/metrics/catalogue/application/interaction/

# Usage: make custom-unit-tests TEST_PATH=tests/metrics/catalogue/infrastructure/test_controller.py::test_when_metric_created_with_existent_parent
custom-unit-tests:
	docker-compose -f docker-compose.test.yml run -e FLASK_ENV=test -e ENVIRONMENT=test --rm metrics-api pytest "$(TEST_PATH)" -s -vvv

integration-tests:
	docker exec -i analytics-challenge_localdb_1 psql -U metricsdbuser -c "DROP DATABASE IF EXISTS testmetricsdb;" postgres;
	docker exec -i analytics-challenge_localdb_1 psql -U metricsdbuser -c "CREATE DATABASE testmetricsdb;" postgres;
	docker-compose -f docker-compose.test.yml run -e FLASK_ENV=test -e ENVIRONMENT=test --rm metrics-api pytest -vvv tests/

# Usage: make custom-integration-tests TEST_PATH=tests/metrics/catalogue/infrastructure/test_controller.py::test_when_metric_created_with_existent_parent
custom-integration-tests:
	docker exec -i analytics-challenge_localdb_1 psql -U metricsdbuser -c "DROP DATABASE IF EXISTS testmetricsdb;" postgres;
	docker exec -i analytics-challenge_localdb_1 psql -U metricsdbuser -c "CREATE DATABASE testmetricsdb;" postgres;
	docker-compose -f docker-compose.test.yml run -e FLASK_ENV=test -e ENVIRONMENT=test --rm metrics-api pytest "$(TEST_PATH)" -s -vvv
