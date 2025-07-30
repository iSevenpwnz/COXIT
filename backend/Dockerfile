# Use uv for fast Python dependency management
FROM python:3.11-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy project configuration
COPY pyproject.toml .
COPY requirements.txt .

# Install dependencies with uv (much faster than pip)
RUN uv pip install --system -r requirements.txt

# Copy source code
COPY . .

# Create storage directories
RUN mkdir -p /app/storage/pdfs /app/storage/summaries /app/storage/meta

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]