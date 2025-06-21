# Python 3.11.8 ベースイメージ
FROM python:3.11.8-slim

# システムパッケージのインストール
RUN apt-get update && \
    apt-get install -y gcc build-essential portaudio19-dev ffmpeg git curl && \
    rm -rf /var/lib/apt/lists/*

# 作業ディレクトリを /app に設定
WORKDIR /app

# pip更新
RUN pip install --upgrade pip setuptools

# 🔽 shared ディレクトリをコンテナにコピー
COPY ../shared /shared

# 🔽 shared を editable モードでインストール
RUN pip install -e /shared

# 🔽 gateway の requirements をコピーしてインストール
COPY gateway/requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

# 🔽 gateway のアプリコードをコピー
COPY gateway /app

# アプリ起動
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--reload"]
