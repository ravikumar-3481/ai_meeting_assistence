# ==============================================================================
# Multi-Stage Production Dockerfile for AI Meeting Assistance Backend
# ==============================================================================
# Architecture:
#   Stage 1 (builder): Compiles C extensions and installs wheel dependencies
#                      into an isolated virtual environment (/opt/venv).
#   Stage 2 (runner):  Minimal Debian Bookworm Slim runtime containing only
#                      runtime system packages (ffmpeg, curl, ca-certificates),
#                      the pre-built /opt/venv, and application code.
#
# Security & Best Practices:
#   - Runs as a dedicated non-root user (appuser:appuser, UID 10001).
#   - Least-privilege filesystem permissions on working and data directories.
#   - Multi-stage build discards compilers (gcc, g++, headers), shrinking attack
#     surface and image footprint.
#   - Native healthcheck hitting /health to enable orchestration auto-healing.
#   - Graceful termination via 'exec' signal propagation (SIGTERM/SIGINT).
#   - Dynamic $PORT binding (compatible with Docker, Cloud Run, Render, K8s).
# ==============================================================================

# ------------------------------------------------------------------------------
# Stage 1: Build Stage
# ------------------------------------------------------------------------------
FROM python:3.12-slim-bookworm AS builder

# Prevent Python from writing .pyc files and buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /build

# Install compilation build dependencies for native wheels (e.g. bcrypt, scikit-learn)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Create dedicated virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Upgrade core packaging tools
RUN pip install --upgrade pip setuptools wheel

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Remove unnecessary compiled test files and package caches inside virtualenv
RUN find /opt/venv -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true \
    && find /opt/venv -type f -name "*.pyc" -delete 2>/dev/null || true

# ------------------------------------------------------------------------------
# Stage 2: Runtime Stage
# ------------------------------------------------------------------------------
FROM python:3.12-slim-bookworm AS runner

# Set production runtime environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH" \
    PORT=8000 \
    UVICORN_WORKERS=1 \
    APP_HOME="/app"

# Install only essential runtime system packages:
#   - ffmpeg: required by pydub, ffmpeg-python, and yt-dlp for audio transcoding
#   - ca-certificates: TLS/SSL verification for external AI services
#   - curl: network diagnostics and container orchestration
#   - tzdata: timezone consistency across audit logging
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    ca-certificates \
    curl \
    tzdata \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Create a secure, non-privileged system user and group (UID/GID 10001)
RUN groupadd -g 10001 appuser \
    && useradd -u 10001 -g appuser -d /app -s /bin/bash -M -c "App User" appuser

WORKDIR ${APP_HOME}

# Copy virtual environment from builder stage
COPY --from=builder /opt/venv /opt/venv

# Create required runtime directories and set ownership to non-root user
RUN mkdir -p ${APP_HOME}/data/downloads \
             ${APP_HOME}/data/outputs \
             ${APP_HOME}/data/uploads \
             /app/logs \
    && chown -R appuser:appuser ${APP_HOME}

# Copy application source code with non-root ownership
COPY --chown=appuser:appuser . ${APP_HOME}

# Copy and configure entrypoint script
COPY --chown=appuser:appuser docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Switch to non-root user
USER appuser

# Expose standard application port
EXPOSE 8000

# Container Healthcheck (polls /health endpoint using standard python urllib)
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD python -c "import urllib.request, os; port = os.environ.get('PORT', '8000'); urllib.request.urlopen(f'http://127.0.0.1:{port}/health')" || exit 1

# Launch application via entrypoint script
ENTRYPOINT ["docker-entrypoint.sh"]

# Default command: start FastAPI application with Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0"]
