from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from phoenix.trace.langchain import LangChainInstrumentor
import os

class OpenTelemetrySetup:
    def __init__(self, service_name="my-langchain-service", collector_endpoint="http://localhost:4317"):
        self.service_name = service_name
        self.collector_endpoint = collector_endpoint
        self.provider = None
        self._setup_environment()
        self._setup_tracing()

    def _setup_environment(self):
        if 'PHOENIX_PROJECT_NAME' not in os.environ:
            os.environ['PHOENIX_PROJECT_NAME'] = self.service_name

    def _setup_tracing(self):
        resource = Resource(attributes={"service.name": self.service_name})
        self.provider = TracerProvider(resource=resource)
        otlp_exporter = OTLPSpanExporter(endpoint=self.collector_endpoint)
        span_processor = BatchSpanProcessor(otlp_exporter)
        self.provider.add_span_processor(span_processor)
        trace.set_tracer_provider(self.provider)
        LangChainInstrumentor().instrument()

    def get_tracer(self, tracer_name):
        return trace.get_tracer(tracer_name)
