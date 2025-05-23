from abc import ABC, abstractmethod
from typing import Any


class Integration(ABC):
    @abstractmethod
    # 実行
    def execute(self, system_prompts: list[Any], user_prompt: list[Any]) -> str:
        pass
