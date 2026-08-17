package telemetry

import (
	"context"
	"strings"

	"github.com/gocql/gocql"
	"go.opentelemetry.io/otel"
	"go.opentelemetry.io/otel/attribute"
	"go.opentelemetry.io/otel/trace"
	"go.opentelemetry.io/otel/codes"
)

const scyllaInstrumentationName = "employee-api/scylladb"

// ScyllaQueryObserver creates OpenTelemetry client spans for ScyllaDB/CQL queries.
// The gocql observer receives the query context, so WithContext(requestCtx) keeps
// the ScyllaDB span inside the originating HTTP trace.
type ScyllaQueryObserver struct {
	tracer trace.Tracer
}

// NewScyllaQueryObserver creates a ScyllaDB query observer using the global tracer provider.
func NewScyllaQueryObserver() *ScyllaQueryObserver {
	return &ScyllaQueryObserver{
		tracer: otel.Tracer(scyllaInstrumentationName),
	}
}

// ObserveQuery records one span for each CQL query executed by the gocql driver.
func (o *ScyllaQueryObserver) ObserveQuery(ctx context.Context, observed gocql.ObservedQuery) {
	if ctx == nil {
		ctx = context.Background()
	}

	operation := cqlOperation(observed.Statement)
	spanName := operation
	if observed.Keyspace != "" {
		spanName += " " + observed.Keyspace
	}

	_, span := o.tracer.Start(
		ctx,
		spanName,
		trace.WithSpanKind(trace.SpanKindClient),
		trace.WithTimestamp(observed.Start),
	)

	span.SetAttributes(
		attribute.String("db.system", "cassandra"),
		attribute.String("db.name", observed.Keyspace),
		attribute.String("db.namespace", observed.Keyspace),
		attribute.String("db.operation", operation),
		attribute.String("db.operation.name", operation),
		attribute.String("db.statement", observed.Statement),
	)

	if observed.Host != nil {
		span.SetAttributes(attribute.String("server.address", observed.Host.ConnectAddress().String()))
	}

	if observed.Rows >= 0 {
		span.SetAttributes(attribute.Int("db.cassandra.rows.returned", observed.Rows))
	}

	if observed.Err != nil {
		span.RecordError(observed.Err)
		span.SetStatus(codes.Error, observed.Err.Error())
	}

	span.End(trace.WithTimestamp(observed.End))
}

func cqlOperation(statement string) string {
	fields := strings.Fields(statement)
	if len(fields) == 0 {
		return "CQL"
	}
	return strings.ToUpper(fields[0])
}
