import io
from fastapi import FastAPI, WebSocket
from pydantic import BaseModel
import speech_recognition as sr
from pydub import AudioSegment

from agents.langgraph.graph import create_graph


# システムの状態を管理するクラス
class QAState:
    def __init__(self, question: str):
        self.question = question
        self.response = None
        self.summary = None
        self.audio_url = None
        self.next = None

graph = create_graph()

# ワークフローの実行
def run_workflow(question: str):
    state = QAState(question).__dict__  # ✅ `dict` に変換
    result = graph.invoke({"state": state})  # ✅ `state` を `dict` にして渡す
    return result["state"]  # ✅ `dict` から `audio_url` を取得


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
    print('downloadWav')
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
        print(e)
    finally:
        return response


"""
Google Speech Recognition で文字起こし
"""
def convertSpeech2Text():
    response = {
        "status": True,
        "message": ''
    }
    recognizer = sr.Recognizer()
    file_path = "data/uploads/received_audio.wav"
    with sr.AudioFile(file_path) as source:
        audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio, language="ja-JP")
            response['message'] = text
            print("文字起こし結果:", text)
        except sr.UnknownValueError as e:
            response['status'] = False
            response['message'] = e
            print(e)
        except sr.RequestError as e:
            print('えーら')
            response['status'] = False
            response['message'] = e
            print(e)
        finally:
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
        print(f"エラー: {e}")
        response['status'] = False
        response['message'] = e
    return response

import time

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    # 音声ファイルの作成
    data = await websocket.receive_bytes()
    downloadWav(data)

    # 音声ファイルをテキストへ変換
    speech = convertSpeech2Text()

    # AIエージェント起動
    if speech['status']:
        print(speech['message'])
        await websocket.send_json({speech['message']})
        audio_output = run_workflow(speech['message'])
        print(audio_output)
        print(audio_output['summary'])
        await websocket.send_json({'message': audio_output['summary']})
    
    # 回答用の音声ファイルを送信
    await sendMP3(websocket=websocket, file_path="data/outputs/output.mp3")
    await websocket.close() # WebSocket を切断

@app.post("/test")
def ask(request: AskRequest):
    question = request.question
    audio_output = run_workflow(question)

    return {"message": "Good bye."}


from agents.integration.gemini_llm import GeminiLLM
from agents.integration.qdrant_database import QdrantDB
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext

@app.post("/init")
def ask(request: AskRequest):
    documents = SimpleDirectoryReader("./knowledge").load_data()
    llm = GeminiLLM()

    qdrant_db = QdrantDB()
    vector_store = qdrant_db.get_store()

    # ストレージコンテキストを作成
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
        llm=llm
    )
    return {"message": "アップロード完了しました"}
