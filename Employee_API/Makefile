APP_VERSION ?= v0.1.0
IMAGE_REGISTRY ?= quay.io/opstree
IMAGE_NAME ?= employee-api

# Get the currently used golang install path (in GOPATH/bin, unless GOBIN is set)
ifeq (,$(shell go env GOBIN))
GOBIN=$(shell go env GOPATH)/bin
else
GOBIN=$(shell go env GOBIN)
endif


# Build


# Build employee binary
build: fmt
	go build -o employee-api


# Code Quality


# Run go fmt against code
fmt:
	go fmt ./...

# Run go vet against code
vet:
	go vet ./...


# Docker


docker-build:
	docker build -t ${IMAGE_REGISTRY}/${IMAGE_NAME}:${APP_VERSION} -f Dockerfile .

docker-push:
	docker push ${IMAGE_REGISTRY}/${IMAGE_NAME}:${APP_VERSION}


# Swagger


swagger:
	swag init -g main.go


# Database Migration
# If DATABASE_URL is not supplied, read it from migration.json
DATABASE_URL ?= $(shell jq -r '.database' migration.json)

run-migrations:
	@echo "========================================="
	@echo "Running Employee DB Migrations"
	@echo "========================================="
	@echo "Database: $(DATABASE_URL)"
	@echo "========================================="

	migrate \
		-source file://migration \
		-database "$(DATABASE_URL)" \
		up