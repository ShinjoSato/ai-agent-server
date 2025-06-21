import os
import time
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import asyncio
import websockets
import json

from shared.utils.socket import print_hello

app = FastAPI()


@app.get("/")
def read_root():
    print_hello()
    return {"message": "Hello, gate2way!"}


@app.websocket("/ws/text")
async def receive_text(websocket: WebSocket):
    print("テキストメッセージ")
    await websocket.accept()
    text = await websocket.receive_text()
    await connect_2_llm_server(websocket=websocket, message=text)


@app.websocket("/ws/speech")
async def receive_speech(websocket: WebSocket):
    print("音声メッセージ")
    await websocket.accept()

     # 音声ファイルの作成
    data = await websocket.receive_bytes()
    download_wav(data)

    # 音声ファイルをテキストへ変換
    speech = await convert_speech_2_text(websocket=websocket)
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
            print("サーバー2が正常に接続を終了しました")
        except WebSocketDisconnect:
            print("クライアントが切断されました")
        finally:
            print("接続終了処理を実行します")
            await websocket.close()
