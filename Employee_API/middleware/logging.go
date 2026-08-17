package middlewares

import (
	"os"
	"time"

	"github.com/gin-gonic/gin"
	log "github.com/sirupsen/logrus"

	"go.opentelemetry.io/otel/trace"
)

func LoggingMiddleware() gin.HandlerFunc {

	// Read service name from environment variable
	serviceName := os.Getenv("OTEL_SERVICE_NAME")
	if serviceName == "" {
		serviceName = "employee-api"
	}

	return func(ctx *gin.Context) {

		startTime := time.Now()

		ctx.Next()

		latency := time.Since(startTime)

		span := trace.SpanFromContext(ctx.Request.Context())
		spanCtx := span.SpanContext()

		traceID := ""
		spanID := ""

		if spanCtx.IsValid() {
			traceID = spanCtx.TraceID().String()
			spanID = spanCtx.SpanID().String()
		}

		log.WithFields(log.Fields{
			"timestamp":        time.Now().UTC().Format(time.RFC3339Nano),
			"severity":         "INFO",
			"service.name":     serviceName,
			"trace_id":         traceID,
			"span_id":          spanID,
			"http.method":      ctx.Request.Method,
			"http.route":       ctx.FullPath(),
			"http.target":      ctx.Request.RequestURI,
			"http.status_code": ctx.Writer.Status(),
			"client.address":   ctx.ClientIP(),
			"latency_ns":       latency.Nanoseconds(),
		}).Info("HTTP REQUEST STATUS")
	}
}