# Dockerfile
FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    APP_PORT=5000

RUN echo "hello there"

# Системные пакеты (минимум; для многих либ хватает этого)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
  && rm -rf /var/lib/apt/lists/*

COPY . /app
WORKDIR /app
# Зависимости
RUN python -m venv .venv
RUN source .venv/bin/activate
# Copy the requirements file into the container and install the dependencies

RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
ENTRYPOINT ['python']

# Expose the port the Flask app runs on (default is 5000)
EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]

# EXPOSE 8000

# CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]