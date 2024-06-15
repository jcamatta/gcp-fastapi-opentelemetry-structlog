#!/bin/sh

gunicorn src.main:app \
    --timeout 0 \
    --preload \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind ":${PORT}" \
    --workers ${NUM_WORKERS} \
    --threads ${NUM_THREADS} \
    --max-requests ${MAX_REQUESTS} \
    --max-requests-jitter ${MAX_REQUESTS_JITTER}