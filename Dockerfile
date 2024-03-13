# using slim version
FROM python:3.10.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r ./requirements.txt

RUN apt-get update && \
    apt-get install -y curl sqlite3 && \
    pip install --upgrade pip && \
    pip install -r ./requirements.txt

COPY . /app

EXPOSE 8000

CMD ["sh", "-c", "python secret_manager.py && uvicorn main:app --reload --host=0.0.0.0"]
