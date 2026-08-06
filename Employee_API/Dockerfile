# ==================================================
# Stage 1 - Build Employee API
# ==================================================
FROM golang:1.25.1 AS builder

WORKDIR /go/src/employee-api

# Install required packages
RUN apt-get update && \
    apt-get install -y wget make jq

# Copy dependency files
COPY go.mod go.sum ./

# Download Go dependencies
RUN go mod download

# Copy source code
COPY . .

# Build application
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 \
    go build -o employee-api main.go

# Download migrate binary
RUN wget -qO- \
https://github.com/golang-migrate/migrate/releases/latest/download/migrate.linux-amd64.tar.gz \
| tar -xz -C /tmp

# ==================================================
# Stage 2 - Runtime
# ==================================================
FROM alpine:3.21

LABEL authors="Opstree Solution" \
      application="Employee API" \
      version="v0.1.0"

WORKDIR /

# Runtime packages
RUN apk add --no-cache \
    bash \
    curl \
    make \
    jq \
    netcat-openbsd \
    ca-certificates

# Copy application
COPY --from=builder /go/src/employee-api/employee-api /employee-api

# Copy config
COPY --from=builder /go/src/employee-api/config.yaml /config.yaml

# Copy migration files
COPY --from=builder /go/src/employee-api/migration /migration

# Copy Makefile
COPY --from=builder /go/src/employee-api/Makefile /Makefile

# Copy migrate binary
COPY --from=builder /tmp/migrate /usr/local/bin/migrate


EXPOSE 8080

ENTRYPOINT ["/employee-api"]
