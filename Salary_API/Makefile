APP_VERSION ?= v0.1.0
IMAGE_REGISTRY ?= quay.io/opstree
IMAGE_NAME ?= salary-api

# Build salary api
build:
	mvn clean package

# Run checkstyle against code
fmt:
	mvn checkstyle:checkstyle

# Run jacoco test cases for coverage
test:
	mvn test

docker-build:
	docker build -t ${IMAGE_REGISTRY}/${IMAGE_NAME}:${APP_VERSION} -f Dockerfile .

docker-push:
	docker push ${IMAGE_REGISTRY}/${IMAGE_NAME}:${APP_VERSION}

# Read from migration.json unless DATABASE_URL is passed
DATABASE_URL ?= $(shell [ -f migration.json ] && jq -r '.database' migration.json)

run-migrations:
	@echo "Running Salary DB Migrations..."
	@echo "Database: $(DATABASE_URL)"

	migrate \
		-source file://migration \
		-database "$(DATABASE_URL)" \
		up