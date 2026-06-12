FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml* requirements.txt* ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

ENV PORT 8000
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "a_core.asgi:application"]
