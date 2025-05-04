# Python 3.11.8 ベースイメージを指定
FROM python:3.11.8-slim

# システムパッケージのインストール
RUN apt-get update && \
    apt-get install -y gcc build-essential portaudio19-dev ffmpeg git && \
    rm -rf /var/lib/apt/lists/*

# 作業ディレクトリ
WORKDIR /app

# 依存ファイルをコピーしてインストール
COPY requirements.txt .

# pip更新
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# アプリケーションコードをコピー
COPY . /app

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--reload"]