# 构建阶段
FROM python:3.9-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 生产阶段
FROM python:3.9-slim
WORKDIR /app
COPY --from=builder /app .
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages

EXPOSE 8000
CMD ["python", "app.py"] 