FROM python:3.12-slim

WORKDIR /app
ENV PYTHONPATH=/app/src \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src

# Treina o modelo na build (artefato fica pronto na imagem).
RUN python -m mlapi.train

EXPOSE 8000
CMD ["uvicorn", "mlapi.api:app", "--host", "0.0.0.0", "--port", "8000"]
