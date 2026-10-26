FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PYTHONPATH=/app/src
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src ./src
COPY web ./web

EXPOSE 8086
CMD ["gunicorn", "--bind", "0.0.0.0:8086", "--workers", "1", "--timeout", "300", "api:app"]
