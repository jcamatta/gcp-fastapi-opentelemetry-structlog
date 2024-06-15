import logging
import structlog
from src.core.config import PROJECT_ID, CLOUD


def _source_location(logger: object, method: str, event_dict: dict) -> dict:

    tmp = {
        "file": event_dict.pop("filename"),
        "line": event_dict.pop("lineno"),
        "function": event_dict.pop("func_name"),
    }

    event_dict["logging.googleapis.com/sourceLocation"] = tmp
    return event_dict

def _format_telemetry(logger: object, method: str, event_dict: dict) -> dict:

    if "trace" in event_dict:
        event_dict["trace"] = hex(event_dict["trace"])
        event_dict["logging.googleapis.com/trace"] = f"projects/{PROJECT_ID}/traces/{event_dict.pop('trace')}"

    if "spanId" in event_dict:
        event_dict["logging.googleapis.com/spanId"] = hex(event_dict.pop("spanId"))
    return event_dict


def _inside_context(logger: object, method: str, event_dict: dict) -> dict:

    ignore = [
        "message",
        "severity", 
        "status",
        "logging.googleapis.com/trace",
        "logging.googleapis.com/spanId",
        "httpRequest",
        "logging.googleapis.com/sourceLocation"
    ]
    
    new_event_dict = {
        "context": {}
    }
    for key, value in event_dict.items():
        if key not in ignore:
            new_event_dict["context"][key] = value
        else:
            new_event_dict[key] = value
    return new_event_dict

def _severity(logger: object, method: str, event_dict: dict) -> dict:
    method = method.upper()
    event_dict["severity"] = method
    return event_dict

def init_logger_config():

    shared_processors = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.EventRenamer("message"),
        structlog.processors.format_exc_info,
        structlog.processors.CallsiteParameterAdder(
            [
                structlog.processors.CallsiteParameter.FUNC_NAME,
                structlog.processors.CallsiteParameter.LINENO,
                structlog.processors.CallsiteParameter.FILENAME,
            ]
        ),
    ]

    if CLOUD:
        domain_processors = [
            _source_location,
            _severity,
            _format_telemetry,
            _inside_context,
        ]

    structlog.configure(
        cache_logger_on_first_use=True,
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        processors=shared_processors + domain_processors + [structlog.processors.JSONRenderer()])