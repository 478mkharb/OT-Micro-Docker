FROM python:3.11-slim

LABEL authors="Opstree Solution" \
      application="Scylla Sync Service" \
      version="v0.1.0"

WORKDIR /app

RUN apt-get update && \
    apt-get install -y gcc python3-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY scylla_to_es_sync.py .

CMD ["python", "scylla_to_es_sync.py"]