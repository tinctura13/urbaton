FROM python:3.9

WORKDIR /app

COPY app.py /app
COPY font.ttf /app

RUN pip install --no-cache-dir fastapi uvicorn Pillow python-multipart

EXPOSE 80

ENV NAME World

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
