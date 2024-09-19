FROM python:3.12-slim

RUN apt-get update && apt-get install -y libpq-dev

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

ENV PYTHONPATH=/app/app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--reload"]
