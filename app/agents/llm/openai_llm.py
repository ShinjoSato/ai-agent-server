import os
from openai import OpenAI
from dotenv import load_dotenv

from langsmith.wrappers import wrap_openai

# .env ファイルをロード
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai_client = wrap_openai(OpenAI(api_key=OPENAI_API_KEY))

from agents.llm.base_llm import BaseLLM

# OpenAIクライアント
class OpenAILLM(BaseLLM):
    def __init__(self):
        self.system_prompts = []
        self.user_prompts = []

    def prepare(self, system_prompts: list[str], user_prompts: list[str]):
        self.system_prompts = [{"role": "system", "content": prompt} for prompt in system_prompts]
        self.user_prompts = [{"role": "user", "content": prompt} for prompt in user_prompts]

    def execute(self, system_prompts: list[str], user_prompt: list[str]):
        self.prepare(system_prompts=system_prompts, user_prompts=user_prompt)
        response = openai_client.chat.completions.create(model="gpt-4o-mini", messages=self.system_prompts + self.user_prompts)
        return response.choices[0].message.content
