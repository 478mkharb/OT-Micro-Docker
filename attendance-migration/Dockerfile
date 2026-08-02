FROM eclipse-temurin:17-jre-alpine

LABEL authors="Opstree Solution" \
      application="Attendance Migration" \
      version="v0.1.0"

RUN apk add --no-cache \
    bash \
    curl \
    wget \
    unzip \
    netcat-openbsd

# Install Liquibase
RUN wget -q https://github.com/liquibase/liquibase/releases/download/v4.33.0/liquibase-4.33.0.zip && \
    unzip -q liquibase-4.33.0.zip -d /opt/liquibase && \
    rm liquibase-4.33.0.zip

ENV PATH="/opt/liquibase:${PATH}"

# PostgreSQL JDBC Driver
RUN wget -q \
https://jdbc.postgresql.org/download/postgresql-42.7.7.jar \
-O /opt/liquibase/lib/postgresql.jar

WORKDIR /migration

COPY Attendance_API/migration ./migration

COPY attendance-migration/entrypoint.sh .

RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]