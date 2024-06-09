FROM --platform=linux/amd64 python:3.9-slim
# FROM python:3.9-slim

# 更新包列表并安装必要的依赖
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# 安装 pip 和 pipenv
RUN pip install --no-cache-dir pipenv

# 复制 Pipfile 和 Pipfile.lock 并安装依赖
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock
RUN pipenv install --deploy --ignore-pipfile

# 复制应用程序代码
COPY ./app /app

# 设置工作目录
WORKDIR /app

# 暴露应用程序端口
EXPOSE 443

# 启动命令
CMD ["pipenv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "443"]
