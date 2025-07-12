import os
import requests
import json
from utils.util import get_logger

ngrok_url = os.getenv("NGROK_URL")


def post_whisper_api(data: dict) -> requests.Response:
    """
    外部のサーバーでwhisperを実行する。
    """
    get_logger().info('post whispoer api')
    url = os.getenv("RUNPOD_API_URL")
    api_key = os.getenv("RUNPOD_API_KEY")

    return requests.post(
        url,
        headers={
            'Content-Type': 'application/json',
            "Authorization": f"Bearer {api_key}"
        },
        data=json.dumps(data)
    )
