FROM python:3.12

WORKDIR /app

ENV PYTHONPATH=/app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY backend ./backend
COPY database ./database
COPY config.py .

CMD ["uvicorn","backend.app.main:app","--host","0.0.0.0","--port","8000"]