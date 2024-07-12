from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export import ConsoleSpanExporter

def setup_tracing(app):
    trace.set_tracer_provider(TracerProvider())
    tracer_provider = trace.get_tracer_provider()

    # Configure the Console exporter
    console_exporter = ConsoleSpanExporter()
    span_processor = SimpleSpanProcessor(console_exporter)
    tracer_provider.add_span_processor(span_processor)

    FlaskInstrumentor().instrument_app(app)
    RequestsInstrumentor().instrument()
