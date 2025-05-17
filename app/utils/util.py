import sys
from datetime import datetime
import io
from pydub import AudioSegment
from loguru import logger


"""
ロガーの取得
"""
def get_logger():
    # 重複回避のため、既存のハンドラをすべて削除
    logger.remove()
    logger.add(sys.stderr, format="{time} {level} {message}", level="DEBUG")
    logger.add(f"logs/{datetime.now().strftime('%Y%m%d')}.log")
    return logger


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
