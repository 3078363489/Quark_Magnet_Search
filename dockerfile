 # 建立 python3.8.10 环境
 FROM python:3.8.10-slim


 MAINTAINER CL

 # 设置 python 环境变量
 ENV PYTHONUNBUFFERED 1

 RUN mkdir -p /var/www/html/Magnet_Search

 # 将 myproject 文件夹为工作目录
 WORKDIR /var/www/html/Magnet_Search

 # 将当前目录加入到工作目录中（. 表示当前目录）
 ADD . /var/www/html/Magnet_Search

 # 更新pip版本
 RUN /usr/local/bin/python -m pip install --upgrade pip

# 使用清华大学的 Debian 镜像源
# 替换原有的软件源配置
RUN echo "deb http://archive.debian.org/debian buster main" > /etc/apt/sources.list && \
    echo "deb http://archive.debian.org/debian-security buster/updates main" >> /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        default-libmysqlclient-dev \
        gcc && \
    rm -rf /var/lib/apt/lists/*
 # 利用 pip 安装依赖
 RUN pip install -r requirements.txt

 CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "--preload", "--access-logfile", "-", "--error-logfile", "-", "Magnet_Search.wsgi:application"]