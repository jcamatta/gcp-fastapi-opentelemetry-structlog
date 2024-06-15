from typing import Callable, Any
from functools import wraps
from datetime import datetime
from inspect import signature


def log(func: Callable) -> Callable:

    import structlog
    from src.core.tracer import tracer, trace

    logger = structlog.stdlib.get_logger()

    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:

        with tracer.start_as_current_span(name=func.__name__) as span:
            
            context = span.get_span_context()
            
            start = datetime.now()

            sig = signature(func)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()

            context = {
                "functionName": func.__name__,
                "trace": context.trace_id,
                "spanId": context.span_id,
            }

            with structlog.contextvars.bound_contextvars(**context):
                
                try:
                    logger.info(f"FUNCION [{func.__name__}] EJECUTADA", functionInput=bound_args.arguments,)

                    output = func(*args, **kwargs)
                    duration = (datetime.now() - start).seconds
                    
                    logger.info(f"FUNCION [{func.__name__}] COMPLETADA", duration=duration, functionOutput=output)
                   
                    return output
                    
                except Exception as error:
                    logger.exception(error)
                    raise(error)
    return wrapper