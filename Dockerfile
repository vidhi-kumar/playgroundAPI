FROM python:3.8.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r ./requirements.txt

RUN apt-get update && \
    apt-get install -y curl

COPY . /app

EXPOSE 8000

CMD ["python", "secret_manager.py", "&&", "uvicorn", "main:app", "--reload", "--host=0.0.0.0"]
