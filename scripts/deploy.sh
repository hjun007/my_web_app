#!/bin/bash

# 加载环境变量
source .env

# 根据 ENABLE_HTTPS 选择配置文件
if [ "$ENABLE_HTTPS" = "true" ]; then
    echo "启用 HTTPS 模式..."
    
    # 检查 ssl 目录
    if [ ! -d "ssl" ]; then
        mkdir ssl
    fi
    
    # 检查证书是否存在，不存在则生成
    if [ ! -f "ssl/certificate.crt" ]; then
        echo "生成自签名证书..."
        openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
            -keyout ssl/private.key -out ssl/certificate.crt \
            -subj "/CN=$(curl -s ifconfig.me)"
    fi
    
    # 使用 HTTPS 配置
    cp nginx/nginx.conf.https nginx/nginx.conf
else
    echo "使用 HTTP 模式..."
    cp nginx/nginx.conf.http nginx/nginx.conf
fi

# 停止现有容器
docker-compose down

# 重新构建并启动
docker-compose up -d --build

echo "部署完成！" 