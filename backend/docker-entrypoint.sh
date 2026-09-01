#!/bin/sh
set -e

# ==============================================================================
# Docker Container Entrypoint Script
# ==============================================================================
# - Ensures application data directories exist with write access.
# - Injects dynamic $PORT and $UVICORN_WORKERS when running uvicorn.
# - Executes the primary process with 'exec' to preserve signal handling (SIGTERM).
# ==============================================================================

# Ensure data directories exist
mkdir -p /app/data/downloads /app/data/outputs /app/data/uploads /app/logs 2>/dev/null || true

# Default port to 8000 if not provided by host/platform (e.g. Cloud Run, Render)
PORT="${PORT:-8000}"
UVICORN_WORKERS="${UVICORN_WORKERS:-1}"

# If the command is uvicorn, append port and workers dynamically if not specified
if [ "$1" = "uvicorn" ]; then
    # Check if --port was explicitly passed
    case "$*" in
        *--port*)
            exec "$@"
            ;;
        *)
            exec "$@" --port "$PORT" --workers "$UVICORN_WORKERS"
            ;;
    esac
fi

# Fallback: exec whatever command was passed (e.g. bash, pytest, etc.)
exec "$@"
