FROM python:3.11-slim-bullseye

# Prevent .pyc files and enable unbuffered output
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create app user
RUN useradd --create-home appuser

# Set workdir and permissions
WORKDIR /app
COPY --chown=appuser:appuser requirements.txt ./

# Install Python packages
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy code
COPY --chown=appuser:appuser . .

# Switch to non-root
USER appuser

# Expose FastAPI port
EXPOSE 8000

# Start the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
