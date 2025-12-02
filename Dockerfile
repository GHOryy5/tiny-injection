FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create non-root user
RUN useradd -m -u 1000 tinyuser && chown -R tinyuser:tinyuser /app
USER tinyuser

# Create volume for reports
VOLUME ["/app/reports"]

# Default command
CMD ["python", "tinyinject.py", "--help"]
