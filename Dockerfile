
FROM python:3.9-alpine

WORKDIR /app

# 使用国内 pip 源
COPY requirements.txt .
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "app.py"] 