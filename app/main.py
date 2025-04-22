import io
import time
from fastapi import FastAPI, WebSocket
from pydantic import BaseModel
from pydub import AudioSegment
import whisper

from utils.util import get_logger
from agents.langgraph.graph import run_workflow


app = FastAPI()

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


"""
受信したバイナリデータを音声ファイルで保存
"""
def downloadWav(data):
    get_logger().info('downloadWav')
    response = {
        "status": True,
        "message": ''
    }
    try:
        # 受信する音声データを格納
        audio_data = bytearray()
        audio_data.extend(data)
        file_path = "data/uploads/received_audio.wav"
        audio = AudioSegment.from_file(io.BytesIO(audio_data), format="webm")
        audio.export(file_path, format="wav")
    except Exception as e:
        response['status'] = False
        response['message'] = e
        get_logger().error(e)
    finally:
        return response


"""
Google Speech Recognition で文字起こし
"""
def convertSpeech2Text():
    response = {
        "status": True,
        "message": '',
        "language": ''
    }
    file_path = "data/uploads/received_audio.wav"
    try:
        model = whisper.load_model("medium")
        get_logger().info('音声の解析を開始します')
        result = model.transcribe(file_path)
        get_logger().info('解析を終了しました')
        get_logger().info(result)
        response['message'] = result['text']
        response['language'] = result['language']
    except Exception as e:
        get_logger().error(e)
        response['status'] = False
    return response

"""
MP3ファイルを送信
"""
async def sendMP3(websocket, file_path):
    response = {
        'status': True,
        'message': ''
    }
    # chunk_size = 1024 * 64  # 64KB チャンクで送信（改善点: 速度向上）
    try:
        with open(file_path, "rb") as audio_file:
            mp3_data = audio_file.read()
            await websocket.send_bytes(mp3_data)
    except Exception as e:
        get_logger().error(e)
        response['status'] = False
        response['message'] = e
    return response


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    start = time.time()
    await websocket.accept()

    # 音声ファイルの作成
    data = await websocket.receive_bytes()
    downloadWav(data)

    # 音声ファイルをテキストへ変換
    speech = convertSpeech2Text()

    # AIエージェント起動
    if speech['status']:
        get_logger().info(speech['message'])
        await websocket.send_json({'message': speech['message']})
        audio_output = run_workflow(question=speech['message'], language=speech['language'])
        get_logger().info(audio_output)
        get_logger().info(audio_output['summary'])
        await websocket.send_json({'message': audio_output['summary']})
    
    # 回答用の音声ファイルを送信
    await sendMP3(websocket=websocket, file_path="data/outputs/output.mp3")
    await websocket.close() # WebSocket を切断
    end = time.time()
    get_logger().debug(f"処理時間: {end - start}秒")
