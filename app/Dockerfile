# Base image
FROM python:3.10-slim as base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        pkg-config \
        libmariadb-dev \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy requirements file and install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Copy .env file
COPY .env /app/.env

# Make entrypoint.sh executable
COPY entrypoint.sh /app/
RUN chmod +x entrypoint.sh

# Expose the Flask app port
EXPOSE 5000

# Development Stage
FROM base as development
CMD ["flask", "run", "--host", "0.0.0.0"]

# Debugging Stage
FROM base as debugger
RUN pip install debugpy
CMD ["python", "-m", "debugpy", "--listen", "0.0.0.0:5678", "--wait-for-client", "-m", "flask", "run", "-h", "0.0.0.0", "-p", "5000"]

# Testing Stage
FROM base as test
RUN pip install pytest
CMD ["pytest"]

# Production Stage
FROM base as production
ENTRYPOINT ["./entrypoint.sh"]
