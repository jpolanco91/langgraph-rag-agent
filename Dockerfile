FROM python:3.14.3

WORKDIR /rag-agent-server-app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "websocket_server.py"]
