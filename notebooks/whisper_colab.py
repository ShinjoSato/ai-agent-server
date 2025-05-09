# Whisper音声解析アプリケーション
# Google Colabで実行するためのFlaskサーバー

# 1. 必要なパッケージのインストール
!pip install openai-whisper pydub flask pyngrok requests dotenv

# 2. 必要なライブラリのインポート
import whisper
import os
from pydub import AudioSegment
from flask import Flask, request, jsonify
from pyngrok import ngrok
import io
import torch  # PyTorchをインポート
import requests
from urllib.parse import urlparse, parse_qs

from google.colab import userdata

# 3. Flaskアプリケーションの初期化
app = Flask(__name__)

# 4. Whisperモデルの初期化
print("Whisperモデルを初期化中...")
# GPUが利用可能な場合はGPUを使用
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"使用デバイス: {device}")
model = whisper.load_model("small").to(device)
print("モデルの初期化が完了しました")

# 5. 音声解析関数の定義
def transcribe_audio(audio_data):
    try:
        # 一時ファイルとして保存
        temp_wav_path = "temp_input.wav"
        with open(temp_wav_path, "wb") as f:
            f.write(audio_data)

        # Whisperで音声を解析
        result = model.transcribe(temp_wav_path)

        # 一時ファイルを削除
        os.remove(temp_wav_path)

        return {
            "status": True,
            "text": result["text"],
            "language": result["language"]
        }

    except Exception as e:
        print(e)
        return {
            "status": False,
            "error": str(e)
        }

# 6. Doppler用の変数を読み込み、環境変数を更新する。
def update_doppler_secret_from_env(key: str, value: str) -> bool:
    """
    .env から project, config, token を読み込み、
    引数 key, value を指定して Doppler の環境変数を更新する。

    必要な .env 変数:
        DOPPLER_PROJECT
        DOPPLER_CONFIG
        DOPPLER_TOKEN

    引数:
        key: 更新するDopplerのキー名
        value: 設定する値

    戻り値:
        成功: True / 失敗: False
    """
    try:
        # 環境変数から設定を取得
        project = userdata.get('DOPPLER_PROJECT')
        config = userdata.get('DOPPLER_CONFIG')
        token = userdata.get('DOPPLER_TOKEN')

        # 必須項目のチェック
        if not all([project, config, token]):
            print("❌ .env に DOPPLER_PROJECT, DOPPLER_CONFIG, DOPPLER_TOKEN が必要です")
            return False

        # リクエスト準備
        api_url = "https://api.doppler.com/v3/configs/config/secrets"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        payload = {
            "project": project,
            "config": config,
            "secrets": {
                key: value
            }
        }
        response = requests.post(api_url, json=payload, headers=headers)


        if response.status_code == 200:
            print(f"✅ Doppler変数 '{key}' を更新しました")
            return True
        else:
            print(f"❌ APIエラー: {response.status_code} - {response.text}")
            return False

    except Exception as e:
        print(f"❌ 例外発生: {e}")
        return False


# 7. APIエンドポイントの定義
@app.route('/transcribe', methods=['POST'])
def handle_transcribe():
    try:
        # リクエストから音声データを取得
        audio_data = request.get_data()

        if not audio_data:
            return jsonify({
                "status": False,
                "error": "音声データが送信されていません"
            }), 400

        # 音声を解析
        result = transcribe_audio(audio_data)

        return jsonify(result)

    except Exception as e:
        return jsonify({
            "status": False,
            "error": str(e)
        }), 500

# 7. サーバーの起動
if __name__ == '__main__':
    # ngrokの認証トークンを設定
    # 以下の行の「YOUR_AUTH_TOKEN」を、ngrokのダッシュボードから取得した認証トークンに置き換えてください
    ngrok.set_auth_token(userdata.get('NGROK_AUTH_TOKEN'))

    # ngrokのトンネルを開く
    public_url = ngrok.connect(5000)
    print(f"ngrokのURL: {public_url}")

    # Dopplerの環境変数を更新
    update_doppler_secret_from_env("NGROK_URL", public_url.public_url)

    print("サーバーを起動しています...")
    print("ngrokのURLが表示されたら、そのURLにPOSTリクエストを送信できます")
    print("例: curl -X POST -H 'Content-Type: application/octet-stream' --data-binary @audio.wav <ngrok-url>/transcribe")

    # Flaskサーバーを起動
    app.run(host='0.0.0.0', port=5000)

"""
使用方法:
1. ngrokのアカウントを作成し、認証トークンを取得してください
   - https://dashboard.ngrok.com/signup でアカウントを作成
   - https://dashboard.ngrok.com/get-started/your-authtoken で認証トークンを取得
2. スクリプト内の「YOUR_AUTH_TOKEN」を取得した認証トークンに置き換えてください
3. このスクリプトを実行すると、ngrokのURLが表示されます
4. そのURLに対して、WAV形式の音声ファイルをPOSTリクエストで送信します
5. レスポンスとして、テキストと言語がJSON形式で返されます

注意事項:
- 大きな音声ファイルの処理には時間がかかる場合があります
- 一時ファイルは自動的に削除されます
- 音声ファイルはWAV形式である必要があります
- Colabのセッションが切れると、サーバーも停止します
""" 