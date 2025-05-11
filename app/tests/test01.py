from agents.langgraph.graph import run_workflow
from utils.util import get_logger

from models.User import User
from models.Message import Message


if __name__ == '__main__':
    get_logger().info('動作テスト')
   # ユーザーとメッセージをPydantic的に作成（DB保存はしない）
    message = Message(
        message='Hello, world!',
        language='en',
        user=User(
            type=1,
            name='Shinjo',
            voice_url='https://example.com/voice.mp3'
        )
    )
    get_logger().info(message)
    get_logger().info(f"user: {message.user}")
    get_logger().info(message.json())

    # question = 'What will be the weather tomorrow in Tokyo?'
    # audio_output = run_workflow(question=question,  language='en', websocket=None)
    get_logger().info('動作終了')
