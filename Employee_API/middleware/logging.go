package middlewares

import (
    "time"

    "github.com/gin-gonic/gin"
    log "github.com/sirupsen/logrus"

    "go.opentelemetry.io/otel/trace"
)

func LoggingMiddleware() gin.HandlerFunc {
    return func(ctx *gin.Context) {

        startTime := time.Now()

        ctx.Next()

        latencyTime := time.Since(startTime)

        span := trace.SpanFromContext(ctx.Request.Context())
        spanCtx := span.SpanContext()

        traceID := ""
        spanID := ""

        if spanCtx.IsValid() {
            traceID = spanCtx.TraceID().String()
            spanID = spanCtx.SpanID().String()
        }

        log.WithFields(log.Fields{
            "trace_id":    traceID,
            "span_id":     spanID,
            "http_method": ctx.Request.Method,
            "request_uri": ctx.Request.RequestURI,
            "status_code": ctx.Writer.Status(),
            "latency":     latencyTime,
            "client_ip":   ctx.ClientIP(),
        }).Info("HTTP REQUEST STATUS")
    }
}
