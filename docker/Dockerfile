FROM python:3.14-rc-slim-bookworm

# Set environment variables to prevent Python from writing .pyc and buffering logs
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN useradd --create-home appuser

# Set the working directory inside the container
WORKDIR /app

# Switch to the non-root user
USER appuser

# Copy only necessary files (minimizing build context size)
COPY --chown=appuser:appuser requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY --chown=appuser:appuser . .

# Expose the FastAPI default port
EXPOSE 8000

# Running the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]