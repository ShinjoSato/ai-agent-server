import os
import time
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import asyncio
import websockets
import json
import sys
import logging
logger = logging.getLogger(__name__)
# ルートロガーの設定
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# フォーマット
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# ファイル出力用ハンドラ
file_handler = logging.FileHandler('logs/myapp.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

# コンソール出力用ハンドラ
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

from shared.utils.socket import print_hello

app = FastAPI()


@app.get("/")
def read_root():
    print_hello()
    return {"message": "Hello, gate2way!"}


@app.websocket("/ws/text")
async def receive_text(websocket: WebSocket):
    logger.info("テキストメッセージ")
    await websocket.accept()
    text = await websocket.receive_text()
    logger.info(text)
    await connect_2_llm_server(websocket=websocket, message=text)


@app.websocket("/ws/speech")
async def receive_speech(websocket: WebSocket):
    logger.info("音声メッセージ")
    await websocket.accept()

     # 音声ファイルの作成
    data = await websocket.receive_bytes()
    download_wav(data)

    # 音声ファイルをテキストへ変換
    speech = await convert_speech_2_text(websocket=websocket)
    logger.info(speech)
    await connect_2_llm_server(websocket=websocket, message=speech)


async def connect_2_llm_server(websocket: WebSocket, message: str):
    data = {
        "message": message,
        "language": "ja"
    }
    # サーバー2へ接続（1回確立）
    async with websockets.connect("ws://ai-agent-server:8000/ws/llm") as server2_ws:
        try:
            await server2_ws.send(json.dumps(data))
            while True:
                # サーバー2から応答を受信
                server_response = await server2_ws.recv()

                # JSONとしてパース
                response_data = json.loads(server_response)

                # クライアントへ応答
                await websocket.send_json(response_data)
        except websockets.exceptions.ConnectionClosedOK:
            logger.info("サーバー2が正常に接続を終了しました")
        except WebSocketDisconnect:
            logger.info("クライアントが切断されました")
        finally:
            logger.info("接続終了処理を実行します")
            await websocket.close()
