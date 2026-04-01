# Stage 1: Builder
FROM python:3.10-slim AS builder
WORKDIR /app
COPY app/requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Final
FROM python:3.10-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY app/ .
ENV PATH=/root/.local/bin:$PATH
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
