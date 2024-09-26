# 使用官方多平台支援的 Python 版本，基於 bullseye
FROM python:3.10-slim-bullseye

LABEL maintainer="royzhang0704@gmail.com"

# 確保 Python 輸出無緩衝
ENV PYTHONUNBUFFERED=1

# 更新 apt 並安裝最新的 SQLite 版本
RUN apt-get update && \
    apt-get install -y --no-install-recommends sqlite3 && \
    rm -rf /var/lib/apt/lists/*

# 複製需求檔和應用程式代碼
COPY ./requirements.txt /tmp/requirements.txt
COPY ./app /app

# 設定工作目錄
WORKDIR /app

# 暴露 Django 默認的埠號 8000
EXPOSE 8000

# 建立虛擬環境，並使用 pip 安裝依賴
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

# 設定 PATH，確保虛擬環境中的 pip 和 python 可用
ENV PATH="/py/bin:$PATH"

# 設定運行容器時的用戶權限
USER django-user
