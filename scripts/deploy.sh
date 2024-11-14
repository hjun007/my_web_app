#!/bin/bash

if [ ! -f config.ini ]; then
    echo "创建config.ini文件..."
    cp config.ini.example config.ini
fi

# 停止现有容器
docker-compose down

# 重新构建并启动
docker-compose up -d --build

echo "部署完成！" 