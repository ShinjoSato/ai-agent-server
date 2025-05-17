import os
import requests
import time
from fastapi import WebSocket
from utils.util import get_logger

from models.Message import Message
from models.User import User

ngrok_url = os.getenv("NGROK_URL")


"""
MP3ファイルを送信
"""
async def sendMP3(websocket: WebSocket, file_path: str):
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


"""
Google Speech Recognition で文字起こし
"""
async def convertSpeech2Text(websocket: WebSocket):
    response = {
        "status": True,
        "message": '',
        "language": ''
    }
    file_path = "data/uploads/received_audio.wav"
    try:
        get_logger().info('音声の解析を開始します')
        start = time.time()
        # 音声ファイルを読み込む
        with open(file_path, 'rb') as f:
            audio_data = f.read()
        # サーバーにPOSTリクエストを送信
        resp = requests.post(
            f"{ngrok_url}/transcribe",
            data=audio_data,
            headers={'Content-Type': 'application/octet-stream'}
        )        
        # レスポンスをJSONとして解析
        result = resp.json()
        end = time.time()
        get_logger().debug(f"音声ファイル分析処理時間: {end - start}秒")
        get_logger().info('解析を終了しました')
        get_logger().info(result)

        response['message'] = result['text']
        response['language'] = result['language']

        message = Message(
            message=response['message'],
            language=response['language'],
            type=0, # トーク
            status=0, # proceed
            user=User(
                type=1,
                name='Shinjo'
            )
        )
        message_json = message.dict()
        message_json['user'] = message.user.dict()
        get_logger().info(message_json)
        await websocket.send_json(message_json)
    except Exception as e:
        get_logger().error(e)
        response['status'] = False
    return response


"""
メッセージをサーバーに送信する
"""
async def sendMessage(websocket: WebSocket, message: Message, key: str):
    get_logger().info('sendMessageを開始します')
    message_json = message.dict()
    if key == 'user':
        message_json[key] = message.user.dict()
    elif key == 'role':
        message_json[key] = message.role.dict()
    get_logger().info(message_json)
    await websocket.send_json(message_json)