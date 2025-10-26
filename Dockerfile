FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY app3.py .

EXPOSE 5000

CMD ["python", "app3.py"]
