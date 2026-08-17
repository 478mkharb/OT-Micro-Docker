# ScyllaDB OpenTelemetry instrumentation

This version is based on the latest working `notification-auto-sync-email` project.
No Notification, Elasticsearch sync, Redis, Frontend, PostgreSQL, or other application behavior was intentionally changed.

## Employee API

- Added a gocql `QueryObserver` that creates OpenTelemetry client spans for ScyllaDB/CQL queries.
- The observer uses the global OpenTelemetry tracer provider already configured by the Employee API.
- Employee API Scylla queries use `c.Request.Context()` so database spans can remain part of the originating HTTP trace.
- The span records attributes such as `db.system=cassandra`, keyspace, operation, statement, and Scylla server address.

## Salary API

The Salary API already uses the OpenTelemetry Java agent and Spring Data Cassandra. The Docker runtime now explicitly enables:

- `OTEL_INSTRUMENTATION_CASSANDRA_ENABLED=true`
- `OTEL_INSTRUMENTATION_SPRING_DATA_ENABLED=true`

This preserves the existing Java-agent approach rather than adding duplicate manual Cassandra instrumentation.

## Verification target

Employee creation should produce a trace containing:

`POST /api/v1/employee/create` → Redis spans → ScyllaDB/Cassandra span (`INSERT employee_info`)

Salary creation should produce:

`POST /api/v1/salary/create/record` → Spring Data → Cassandra/ScyllaDB span (`INSERT employee_salary`)
