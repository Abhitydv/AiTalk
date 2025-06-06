# Dockerfile for AiTalk

FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY chatbot.py .

CMD ["streamlit", "run", "chatbot.py", "--server.port=8501", "--server.enableCORS=false"]
