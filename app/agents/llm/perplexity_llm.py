import os
from openai import OpenAI
from dotenv import load_dotenv

from langsmith.wrappers import wrap_openai

# .env ファイルをロード
load_dotenv()
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")

# Perplexity クライアントを作成
perplexity_client = wrap_openai(OpenAI(api_key=PERPLEXITY_API_KEY, base_url="https://api.perplexity.ai"))


from agents.llm.openai_llm import OpenAILLM

class PerplexityLLM(OpenAILLM):
    def __init__(self):
        super().__init__()
    
    def prepare(self, system_prompts, user_prompts):
        super().prepare(system_prompts, user_prompts)

    def execute(self, system_prompts: list[str], user_prompt: list[str]):
        self.prepare(system_prompts=system_prompts, user_prompts=user_prompt)
        response = perplexity_client.chat.completions.create(model="sonar", messages=self.system_prompts + self.user_prompts)
        return response.choices[0].message.content