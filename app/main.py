import os
import io
from dotenv import load_dotenv
from langgraph.graph import StateGraph
from fastapi import FastAPI, WebSocket
from pydantic import BaseModel
import speech_recognition as sr
from pydub import AudioSegment

# .env ファイルをロード
load_dotenv()

# APIキーを環境変数から取得
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

# システムの状態を管理するクラス
class QAState:
    def __init__(self, question: str):
        self.question = question
        self.openai_response = None
        self.need_search = None
        self.perplexity_response = None
        self.final_summary = None
        self.audio_url = None
        self.next = None

def end_node(inputs: dict) -> dict:
    state = inputs["state"]
    return {"state": state}

from clients.openai_client import answer_with_openai, check_response_quality, summarize_with_openai
from clients.perplexity_client import search_with_perplexity
from clients.elevenlabs_client import generate_speech

# LangGraphでワークフローを構築
workflow = StateGraph(dict)  # ✅ `dict` を状態として使う

workflow.add_node("answer_with_openai", answer_with_openai)
workflow.add_node("check_response_quality", check_response_quality)
workflow.add_node("search_with_perplexity", search_with_perplexity)
workflow.add_node("summarize_with_openai", summarize_with_openai)
workflow.add_node("generate_speech", generate_speech)
workflow.add_node("end_node", end_node)


workflow.set_entry_point("answer_with_openai")
workflow.add_edge("answer_with_openai", "check_response_quality")
workflow.add_conditional_edges(
    "check_response_quality",
    lambda state: state["next"], {
        "search_with_perplexity": "search_with_perplexity",
        "summarize_with_openai": "summarize_with_openai"
    }
)
workflow.add_edge("search_with_perplexity", "summarize_with_openai")
workflow.add_edge("summarize_with_openai", "generate_speech")
workflow.add_edge( "generate_speech", "end_node")
workflow.set_finish_point("end_node")


# ワークフローのコンパイル
graph = workflow.compile()
# print(graph.get_graph())
# print(graph.get_graph().draw_ascii())


# ワークフローの実行
def run_workflow(question: str):
    state = QAState(question).__dict__  # ✅ `dict` に変換
    result = graph.invoke({"state": state})  # ✅ `state` を `dict` にして渡す
    return result["state"]["audio_url"]  # ✅ `dict` から `audio_url` を取得


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
        file_path = "download/received_audio.wav"
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
    file_path = "download/received_audio.wav"
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
async def sendMP3(websocket):
    response = {
        'status': True,
        'message': ''
    }
    file_path = "output/output.mp3"
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
        await websocket.send_json({'message': 'ユーザー >>' + speech['message']})
        audio_output = run_workflow(speech['message'])
        print(audio_output)
        await websocket.send_json({'message': '要約 >>'})
    
    # 回答用の音声ファイルを送信
    await sendMP3(websocket)
   
    await websocket.send_json({'message': '終了'})
    await websocket.close() # WebSocket を切断
