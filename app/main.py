import os
import time
from fastapi import FastAPI, WebSocket
from pydantic import BaseModel

from utils.util import get_logger, downloadWav
from utils.socket import sendMP3, convertSpeech2Text
from agents.langgraph.graph import run_workflow

app = FastAPI()

ngrok_url = os.getenv("NGROK_URL")

# リクエストボディの定義
class AskRequest(BaseModel):
    question: str

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI test!"}


@app.post("/ask")
def ask(request: AskRequest):
    question = request.question
    return {"question": question, "message": 'メッセージ'}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    start = time.time()
    await websocket.accept()

    # 音声ファイルの作成
    data = await websocket.receive_bytes()
    downloadWav(data)

    # 音声ファイルをテキストへ変換
    speech = await convertSpeech2Text(websocket=websocket)

    # AIエージェント起動
    if speech['status']:
        get_logger().info(speech['message'])
        audio_output = await run_workflow(question=speech['message'], language=speech['language'], websocket=websocket)
        get_logger().info(audio_output)
        get_logger().info(audio_output['summary'])
    
    # 回答用の音声ファイルを送信
    await sendMP3(websocket=websocket, file_path="data/outputs/output.mp3")
    await websocket.close() # WebSocket を切断
    end = time.time()
    get_logger().debug(f"処理時間: {end - start}秒")
