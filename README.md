# 🧠 分身AIエージェント - サーバーサイド（Backend）

<div style="display: flex; justify-content: center;">
    <video controls src="https://github.com/user-attachments/assets/91f5082e-8054-4e4d-974d-65f6d2d1c68b" muted="true"></video>
</div>

このリポジトリは、**音声入力に対して生成AIを用いて分析・返答し、自分の声で返す**ことができる「分身AIエージェント」の**サーバーサイドアプリケーション**です。  
クライアントアプリと連携し、ユーザーとの自然な対話を実現します。


## 📌 概要

- ユーザーがマイクに向かって話しかけると、音声がサーバーに送られます  
- サーバーは音声をテキストに変換し、ChatGPTまたはPerplexityで内容を分析  
- 分析結果に基づいて回答文を生成し、ElevenLabsで合成音声を作成  
- 最終的に音声ファイルをクライアントに返し、ユーザーに音声で返答します  


## 🎥 デモ動画

- 🔗 [日本語版デモ動画のYouTubeリンクはこちら](https://youtu.be/dwX0WjToQKA?si=FqRIrqx9qAHPU2Sb)


## ⚙️ 主な機能（サーバー側）

- FastAPI + WebSocket によるリアルタイム通信
- 音声データを解析し、テキストへ変換
- OpenAI (ChatGPT) / Perplexity による自然言語処理
- ElevenLabs による音声合成（ユーザーの声）
- LangGraph による処理フロー構築
- LangSmith によるログ監視・デバッグ
- Docker / docker-compose による開発・実行環境の構築


## 🛠️ 技術スタック

| 分類       | 使用技術                    |
|------------|-----------------------------|
| サーバー   | Python, FastAPI             |
| AI         | OpenAI API, Perplexity API  |
| 音声合成   | ElevenLabs API              |
| フロー制御 | LangGraph                   |
| デバッグ   | LangSmith                   |
| 実行環境   | Docker, docker-compose      |


## 🚀 セットアップ手順

1. `.env` ファイルを作成  
   `app/.env.example` をコピーして `.env` を作成し、必要なAPIキー等を入力します。

   ```bash
   cp app/.env.example app/.env
   ```

2. Dockerでビルド & 実行

   ```bash
   docker compose up --build
   ```

3. WebSocket接続先  

   ```bash
   ws://127.0.0.1:8000/ws
   ```


## 🔗 クライアントとの連携

このサーバーは以下のクライアントアプリと連携して動作します：  
👉 [分身AIエージェント - フロントエンド](https://github.com/ShinjoSato/ai-agent-server)
