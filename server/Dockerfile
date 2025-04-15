FROM python:3.13-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Comando padrão (sobrescrito pelo docker-compose)
CMD ["python3", "rest/app.py"]
