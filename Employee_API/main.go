package main

import (
	"context"

	docs "employee-api/docs"
	middlewares "employee-api/middleware"
	"employee-api/routes"
	"employee-api/telemetry"

	"github.com/gin-gonic/gin"
	"github.com/penglongli/gin-metrics/ginmetrics"
	"github.com/sirupsen/logrus"

	"go.opentelemetry.io/contrib/instrumentation/github.com/gin-gonic/gin/otelgin"

	swaggerfiles "github.com/swaggo/files"
	ginSwagger "github.com/swaggo/gin-swagger"
)

var router = gin.New()

func init() {
	logrus.SetLevel(logrus.InfoLevel)
	logrus.SetFormatter(&logrus.JSONFormatter{})
}

// @title Employee API
// @version 1.0
// @description The REST API documentation for employee webserver
// @termsOfService http://swagger.io/terms/

// @contact.name Opstree Solutions
// @contact.url https://opstree.com
// @contact.email opensource@opstree.com

// @license.name Apache 2.0
// @license.url http://www.apache.org/licenses/LICENSE-2.0.html

// @BasePath /api/v1
// @schemes http
func main() {

	shutdown, err := telemetry.InitTracer()
	if err != nil {
		logrus.Fatal(err)
	}
	defer shutdown(context.Background())

	monitor := ginmetrics.GetMonitor()
	monitor.SetMetricPath("/metrics")
	monitor.SetSlowTime(1)
	monitor.SetDuration([]float64{0.1, 0.3, 1.2, 5, 10})
	monitor.Use(router)

	router.Use(gin.Recovery())

	router.Use(otelgin.Middleware("employee-api"))

	// Custom Prometheus counter with HTTP status
	router.Use(middlewares.PrometheusMiddleware())

	router.Use(middlewares.LoggingMiddleware())

	v1 := router.Group("/api/v1")

	docs.SwaggerInfo.BasePath = "/api/v1/employee"
	routes.CreateRouterForEmployee(v1)

	url := ginSwagger.URL("/swagger/doc.json")
	router.GET("/swagger/*any", ginSwagger.WrapHandler(swaggerfiles.Handler, url))

	if err := router.Run(":8080"); err != nil {
		logrus.Fatal(err)
	}
}