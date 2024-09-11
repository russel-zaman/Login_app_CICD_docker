# For more information, please refer to https://aka.ms/vscode-docker-python
#The image is built from python:3.10-slim, a minimal Python image.
FROM python:3.10-slim as base           

#EXPOSE 5000 opens port 5000, which is typically used by Flask apps.
EXPOSE 5000

# Prevents Python from creating .pyc files to keep the container clean.
ENV PYTHONDONTWRITEBYTECODE=1

# Ensures output is immediately flushed to the terminal for better container logging.
ENV PYTHONUNBUFFERED=1

# The requirements.txt file is copied to the container, and Python dependencies are installed via pip.
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

#The working directory is set to /app, where the code is copied into
WORKDIR /app
COPY . /app

# A non-root user (appuser) is created to improve security, with access to the application folder. 
# This ensures the container doesn’t run as root.
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# Degguer config
FROM base as debugger
#In this debugger stage, the debugpy package is installed to allow remote debugging.
RUN pip install debugpy
#The container runs Flask with debugpy listening on port 5678 and waits for a debugger client before starting.
CMD ["python", "-m", "debugpy", "--listen", "0.0.0.0:5678", "--wait-for-client", "-m", "flask", "run", "-h","0.0.0.0" , "-p","5000"]

# This stage runs the Flask app in development mode, exposing the server on 0.0.0.0 so it can be accessed from outside the container.
FROM base as debug
CMD ["flask", "run", "--host", "0.0.0.0"]

# The test stage installs pytest and sets the container's command to run tests.
# This is useful for continuous integration or testing environments.
FROM base as test
RUN pip install pytest
CMD ["python","-m","pytest"]


# The prod stage is for production. The Flask app is run, accessible on all network interfaces (0.0.0.0), ready for deployment.
FROM base as prod

CMD ["flask", "run", "--host", "0.0.0.0"]

