import time
from typing import Callable
from contextlib import asynccontextmanager

# ===> FastAPI
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# ===> Observability Logs
from src.core.logger import init_logger_config
# ===> Observability Trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from src.core.tracer import trace_provider, tracer, trace

# ===> Routers
from src.models.base.router import router as base_router


allowed_origins = ["*"]
allowed_methods = ["GET", "POST"]
allowed_headers = ["Content-Type"]


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
        Funcion que se ejecuta antes del manejo de la PRIMERA request
        y despues de la ULTIMA response.
    """
    init_logger_config()
    yield


app = FastAPI(lifespan=lifespan)
FastAPIInstrumentor().instrument_app(app=app, tracer_provider=trace_provider)

# ==> Include the models ...
app.include_router(base_router)

@app.middleware("http")
async def add_http_request(request: Request, call_next: Callable) -> Response:
    """
        Middleware que agrega como contexto a todos los logs informacion de la request en curso.
        Inicia un span master que incluiria a todos los mini-spans que las funciones generen para el manejo de la request.
        Logea el inicio del manejo de la request y el fin de la misma.
    """

    import structlog

    structlog.contextvars.clear_contextvars()
    logger = structlog.stdlib.get_logger()

    http_request = {
        "requestMethod": request.method,
        "requestUrl": str(request.url),
        "requestSize": str(request.__sizeof__()),
        "userAgent": request.headers.get("user-agent", "unknown"),
        "remoteIp": request.client.host,
        "protocol": request.scope.get("type", "unknown")
    }

    structlog.contextvars.bind_contextvars(httpRequest=http_request)

    span_name = f"{request.method} {request.url.path} {request.scope.get('type')}"
    with tracer.start_as_current_span(name=span_name, kind=trace.SpanKind.SERVER) as span:
        context = span.get_span_context()

        await logger.ainfo(f"REQUEST [{span_name}] EJECUTADA", trace=context.trace_id, spanId=context.span_id)

        response: Response = await call_next(request)

        http_request["responseSize"] = str(response.__sizeof__())
        http_request["status"] = response.status_code
        http_request["latency"] = response.headers.get("x-process-time")

        structlog.contextvars.bind_contextvars(httpRequest=http_request)
        
        await logger.ainfo(f"REQUEST [{span_name}] COMPLETADA", trace=context.trace_id, spanId=context.span_id)


    return response

@app.middleware("http")
async def add_process_time_header(request: Request, call_next: Callable) -> Response:
    """
        Middleware que agrega al header del response el tiempo de procesamiento de la request.
    """
    start = time.time()
    response: Response = await call_next(request)
    response.headers["x-process-time"] = str(time.time() - start)
    return response

app.middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_methods=allowed_methods,
    allow_headers=allowed_headers,
)

@app.get("/", response_class=JSONResponse)
async def root(request: Request):
    """
        Punto de inicio o Home de la API.
    """
    return {"working": True}