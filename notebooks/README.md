# Whisper音声解析アプリケーション

Google Colabで実行するための音声解析アプリケーションです。Whisperを使用して音声をテキストに変換します。

## 機能

- 音声ファイル（WAV形式）のテキスト変換
- 複数言語の自動検出
- GPU対応（利用可能な場合）
- WebSocket経由での音声データ受信

## セットアップ手順

1. Google Colabで新しいノートブックを作成

2. 必要なパッケージのインストール
```python
!pip install openai-whisper pydub flask pyngrok
```

3. `whisper_colab.py`の内容をコピーして実行

4. ngrokの認証トークンを設定
   - [ngrokのダッシュボード](https://dashboard.ngrok.com/signup)でアカウントを作成
   - [認証トークン](https://dashboard.ngrok.com/get-started/your-authtoken)を取得
   - スクリプト内の`YOUR_AUTH_TOKEN`を取得したトークンに置き換え

## 使用方法

1. スクリプトを実行すると、ngrokのURLが表示されます

2. 音声ファイルを送信
```bash
curl -X POST -H 'Content-Type: application/octet-stream' --data-binary @audio.wav <ngrok-url>/transcribe
```

3. レスポンス例
```json
{
    "status": true,
    "text": "変換されたテキスト",
    "language": "検出された言語コード"
}
```

## 注意事項

- 音声ファイルはWAV形式である必要があります
- 大きな音声ファイルの処理には時間がかかる場合があります
- 一時ファイルは自動的に削除されます
- Colabのセッションが切れると、サーバーも停止します
- GPUが利用可能な場合は自動的にGPUを使用します

## 技術仕様

- 使用モデル: Whisper small
- 対応言語: 自動検出
- サーバー: Flask
- トンネリング: ngrok
- 音声形式: WAV

## トラブルシューティング

1. 接続エラー
   - ngrokの認証トークンが正しく設定されているか確認
   - Colabのセッションが有効か確認

2. 音声解析エラー
   - 音声ファイルがWAV形式であることを確認
   - 音声ファイルが破損していないか確認

3. パフォーマンス
   - GPUが利用可能な場合は自動的に使用されます
   - 大きな音声ファイルは処理に時間がかかる場合があります 