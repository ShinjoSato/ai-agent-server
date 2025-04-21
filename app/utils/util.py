import sys
from datetime import datetime
from loguru import logger


"""
ロガーの取得
"""
def get_logger():
    # 重複回避のため、既存のハンドラをすべて削除
    logger.remove()
    logger.add(sys.stderr, format="{time} {level} {message}", filter="my_module", level="DEBUG")
    logger.add(f"logs/{datetime.now().strftime('%Y%m%d')}.log")
    return logger
