from opentelemetry import trace, baggage
from opentelemetry.sdk.resources import Resource, ProcessResourceDetector
from opentelemetry.sdk.trace import Tracer, TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter

# context propagation
from opentelemetry.propagate import Context
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from opentelemetry.baggage.propagation import W3CBaggagePropagator

# cloud
from opentelemetry.exporter.cloud_trace import CloudTraceSpanExporter
from opentelemetry.resourcedetector.gcp_resource_detector import GoogleCloudResourceDetector

from starlette.datastructures import Headers

# constants
from src.core.config import CLOUD


def set_trace_provider() -> TracerProvider:
    
    if CLOUD:
        resource = GoogleCloudResourceDetector().detect()
        trace_provider = TracerProvider(resource=resource)
        trace_provider.add_span_processor(SimpleSpanProcessor(CloudTraceSpanExporter()))
    else:
        resource = ProcessResourceDetector().detect()
        trace_provider = TracerProvider(resource=resource)
        trace_provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))
    
    trace.set_tracer_provider(tracer_provider=trace_provider)

    return trace_provider

def extract_telemetry_context(headers: Headers) -> Context:
    carrier = {"traceparent": headers.get("traceparent")}
    ctx = TraceContextTextMapPropagator().extract(carrier)

    b2 = {"baggage": headers.get("baggage")}
    ctx2 = W3CBaggagePropagator().extract(b2, context=ctx)

    return ctx2

def propagate_telemetry_context(context: Context | None = None) -> dict:
    
    headers = dict()
    ctx = baggage.clear() if context is None else context

    W3CBaggagePropagator().inject(headers, ctx)
    TraceContextTextMapPropagator().inject(headers, ctx)
    return headers

trace_provider = set_trace_provider()
tracer = trace.get_tracer(__name__)