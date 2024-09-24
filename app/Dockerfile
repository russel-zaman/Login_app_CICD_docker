# Use the official Python image from the Docker Hub
FROM python:3.10-slim 

# Set environment variables within Docker container
# When it is set to 1, it tells Python not to write .pyc files
ENV PYTHONDONTWRITEBYTECODE 1       
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        pkg-config \
        libmariadb-dev \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app/

COPY entrypoint.sh /app/

# Make entrypoint.sh executable
RUN chmod +x entrypoint.sh

# Expose port 5000
EXPOSE 5000

#FROM base as prod
# Use the custom entry point script
ENTRYPOINT ["./entrypoint.sh"]

#FROM base as unit_test

#CMD ["python", "-m", "pytest", "--cov=login_app_CICD_docker" "--cov-report=term-missing"]
