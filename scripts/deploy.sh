#!/bin/bash

# 检查是否存在.env文件
if [ ! -f .env ]; then
    echo "创建.env文件..."
    cp .env.example .env
fi

if [ ! -f config.ini ]; then
    echo "创建config.ini文件..."
    cp config.ini.example config.ini
fi

# 加载环境变量
source .env

# 停止现有容器
docker-compose down

# 重新构建并启动
docker-compose up -d --build

echo "部署完成！" 