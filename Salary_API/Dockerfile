# ==================================================
# Stage 1 - Build Salary API
# ==================================================
FROM maven:3.9.9-eclipse-temurin-17 AS builder

WORKDIR /workspace

# Install required packages
RUN apt-get update && \
    apt-get install -y wget make jq

# Copy project files
COPY pom.xml .
COPY src/ src/
COPY migration/ migration/
COPY Makefile .


# Build application
RUN mvn clean package -DskipTests

# Download migrate binary
RUN wget -qO- \
https://github.com/golang-migrate/migrate/releases/latest/download/migrate.linux-amd64.tar.gz \
| tar -xz -C /tmp

# ==================================================
# Stage 2 - Runtime
# ==================================================
FROM alpine:3.21

LABEL authors="Opstree Solution" \
      application="Salary API" \
      version="v0.1.0"

WORKDIR /app

# Runtime dependencies
RUN apk add --no-cache \
    openjdk17-jre \
    bash \
    curl \
    make \
    jq \
    netcat-openbsd \
    ca-certificates

# Application
COPY --from=builder /workspace/target/*.jar /app/salary.jar


# Startup script


EXPOSE 8082

ENTRYPOINT ["java","-jar","/app/salary.jar"]