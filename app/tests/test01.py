from agents.langgraph.graph import run_workflow
from utils.util import get_logger


if __name__ == '__main__':
    get_logger().info('動作テスト')
    question = 'What will be the weather tomorrow in Tokyo?'
    audio_output = run_workflow(question=question)
    get_logger().info('動作終了')
