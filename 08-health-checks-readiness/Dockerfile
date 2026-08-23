FROM python:3.12-slim AS builder
WORKDIR /install
COPY requirements.txt .
RUN pip install --prefix=/install/python --no-cache-dir -r requirements.txt

FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /install/python /usr/local
COPY app ./app
EXPOSE 8000
ENV PYTHONUNBUFFERED=1
HEALTHCHECK --interval=30s --timeout=5s --retries=3 CMD python -c "import urllib.request;urllib.request.urlopen('http://127.0.0.1:8000/health')"
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]