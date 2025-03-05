# 使用完整的 Python 3.11 Bullseye 版本
FROM python:3.11-bullseye

LABEL maintainer="royzhang0704@gmail.com"

# Copy requirements files and scripts
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./scripts /scripts
COPY ./app /app

#設置文件的工作目錄為 /app資料夾
WORKDIR /app 

#開放 8000端口  這個應用會在8000端口提供服務
EXPOSE 8000

# Development flag
ARG DEV=false

# Install dependencies and create a virtual environment
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apt-get update && apt-get install -y --no-install-recommends \
        postgresql-client \
        libjpeg-dev \
        zlib1g-dev \
        build-essential \
        libpq-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ "$DEV" = "true" ]; then /py/bin/pip install -r /tmp/requirements.dev.txt ; fi && \
    rm -rf /var/lib/apt/lists/* /tmp && \
    adduser --disabled-password --no-create-home django-user && \
    mkdir -p /vol/web/media && \
    mkdir -p /vol/web/static && \
    chown -R django-user:django-user /vol && \
    chmod -R 755 /vol && \
    chmod -R +x /scripts

# 設定環境變數,讓系統能找到腳本和Python命令
ENV PATH="/scripts:/py/bin:$PATH"

#接下來的指令都用這個低權限使用者執行
USER django-user

# Run the application
CMD ["run.sh"]
