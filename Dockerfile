# Build stage
FROM python:3.10-slim as builder

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --user -r requirements.txt

# Runtime stage
FROM python:3.10-slim

# Create non-root user
RUN useradd -m -u 1000 brainstorm && \
    mkdir -p /app/logs /app/exports && \
    chown -R brainstorm:brainstorm /app

# Set working directory
WORKDIR /app

# Copy Python dependencies from builder
COPY --from=builder /root/.local /home/brainstorm/.local

# Copy application code
COPY --chown=brainstorm:brainstorm . .

# Switch to non-root user
USER brainstorm

# Update PATH
ENV PATH=/home/brainstorm/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app

# Create volumes for persistent data
VOLUME ["/app/logs", "/app/exports"]

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import agents; import core" || exit 1

# Default command
CMD ["python", "main.py"] 