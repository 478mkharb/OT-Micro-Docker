FROM alpine:3.21

LABEL authors="Opstree Solution" \
      application="Scylla Migration" \
      version="v0.1.0"

RUN apk add --no-cache \
    bash \
    curl \
    netcat-openbsd

# Install golang-migrate
RUN curl -L https://github.com/golang-migrate/migrate/releases/download/v4.19.0/migrate.linux-amd64.tar.gz \
    | tar -xz -C /usr/local/bin

RUN chmod +x /usr/local/bin/migrate

WORKDIR /migration

# Copy migration files
COPY scylla-migration/migration ./migration

# Copy startup script
COPY scylla-migration/entrypoint.sh .

RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]