FROM python:3.12-slim
WORKDIR /app
RUN apt-get update && apt-get install -y ca-certificates && update-ca-certificates
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]