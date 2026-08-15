FROM python:3.12-slim
WORKDIR /repo/backend
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/app app
COPY backend/artifacts artifacts
COPY data /repo/data
COPY scenarios /repo/scenarios
COPY benchmark-evidence /repo/benchmark-evidence
CMD ["python","-m","uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]
