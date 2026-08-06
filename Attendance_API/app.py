"""
Module for calling the main flask application.
The application will be only supported with Flask and Gunicorn.
"""
from flask import Flask, json
from flasgger import Swagger
from prometheus_flask_exporter import PrometheusMetrics
from router.attendance import route as create_record
from router.cache import cache
from utils.json_encoder import DataclassJSONEncoder
from client.redis.redis_conn import get_caching_data
from telemetry.telemetry import init_tracing
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from middleware.logging import register_logging

app = Flask(__name__)

init_tracing()
FlaskInstrumentor().instrument_app(app)

register_logging(app)

swagger = Swagger(app)

metrics = PrometheusMetrics(app)
metrics.info("attendance_api", "Attendance API opentelemetry metrics", version="0.1.0")

cache.init_app(app, get_caching_data())

app.config['JSON_SORT_KEYS'] = False
json.provider.DefaultJSONProvider.sort_keys = False
app.json_encoder = DataclassJSONEncoder

app.register_blueprint(create_record, url_prefix="/api/v1")
