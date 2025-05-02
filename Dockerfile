# Builder stage
FROM python:3.11-slim-bookworm@sha256:e1bd87e167040feb40dd75b55cc857c05599a1a74bb951d0499756f0e44737b4 AS builder

WORKDIR /app
COPY requirements.txt .

RUN python -m pip install --upgrade pip && \
    pip install --user --no-cache-dir -r requirements.txt gunicorn

# Runtime stage
FROM python:3.11-slim-bookworm@sha256:e1bd87e167040feb40dd75b55cc857c05599a1a74bb951d0499756f0e44737b4 AS runtime

# Runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd --create-home -u 1001 appuser
USER appuser
WORKDIR /home/appuser

# Copy installed packages from builder
COPY --from=builder --chown=appuser:appuser /root/.local /home/appuser/.local
COPY --chown=appuser:appuser . .

# Ensure .local/bin is in PATH
ENV PATH="/home/appuser/.local/bin:$PATH" \
    PYTHONPATH=/home/appuser/code

# Healthcheck configuration
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl --fail http://localhost:8000/health || exit 1

# Version argument for reproducible builds

# Labels
LABEL maintainer="SchwartzKamel <lafiamafia@protonmail.com>" \
      org.opencontainers.image.title="helloworld_python" \
      org.opencontainers.image.description="Optimized Python application container" \
      org.opencontainers.image.url="https://github.com/SchwartzKamel/docker-python-base" \
      org.opencontainers.image.version="1.0.0" \
      org.opencontainers.image.source="https://github.com/SchwartzKamel/docker-python-base" \
      org.opencontainers.image.licenses="Apache-2.0" \
      security.compliance="cis-docker-1.2.0" \
      security.specs="seccomp=default" \
      security.scan="trivy"

# Runtime command
CMD ["python", "main.py"]

# Trivy security scan
FROM runtime AS trivy-scan
USER root
RUN apt-get update && apt-get install -y --no-install-recommends wget ca-certificates
RUN wget -q https://github.com/aquasecurity/trivy/releases/download/v0.49.1/trivy_0.49.1_Linux-64bit.deb
RUN dpkg -i trivy_0.49.1_Linux-64bit.deb
RUN trivy filesystem --severity CRITICAL --ignore-unfixed /