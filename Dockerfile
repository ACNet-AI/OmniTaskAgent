FROM python:3.11-slim

WORKDIR /app

# Install system dependencies and Node.js
RUN apt-get update && apt-get install -y \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install global Node.js dependencies
RUN npm install -g mcp-shrimp-task-manager

# Copy Python package files
COPY pyproject.toml .
COPY README.md .
COPY .env.example .

# Copy application code
COPY omni_task_agent ./omni_task_agent
COPY run_mcp.py .
COPY adapters.py .

# Install Python dependencies
RUN pip install --no-cache-dir -e .

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Command will be provided by smithery.yaml
# Default command for testing
CMD ["python", "run_mcp.py"] 