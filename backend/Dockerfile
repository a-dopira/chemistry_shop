FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    python3-dev \
    gobject-introspection \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install --upgrade pip --no-warn-script-location

RUN pip install -r requirements.txt --no-cache-dir --no-warn-script-location

COPY . .

CMD ["sh", "/app/entrypoint.sh"]