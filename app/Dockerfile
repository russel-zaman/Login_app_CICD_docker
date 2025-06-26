# Use the official Python image from the Docker Hub
FROM python:3.10-slim as base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    LOG_LEVEL=DEBUG \
    LOG_FILE=/var/log/app/app.log

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        pkg-config \
        libmariadb-dev \
        build-essential \
        rsync \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Create and configure logs directory
RUN mkdir -p /var/log/app \
    && chmod -R 755 /var/log/app

# Make entrypoint script executable and append logging envs
RUN chmod +x entrypoint.sh \
    && echo "export LOG_LEVEL=${LOG_LEVEL}" >> /app/entrypoint.sh \
    && echo "export LOG_FILE=${LOG_FILE}" >> /app/entrypoint.sh

# Expose the Flask port
EXPOSE 5000

##############################
# Production build stage
##############################
FROM base as prod
ENTRYPOINT ["./entrypoint.sh"]

##############################
# Unit testing stage
##############################
# FROM base as unit_test
# CMD ["python", "-m", "pytest", "--cov=login_app_CICD_docker", "--cov-report=term-missing"]

##############################
# Local development stage
##############################
# FROM base as localdev
# CMD ["python", "app.py"]
