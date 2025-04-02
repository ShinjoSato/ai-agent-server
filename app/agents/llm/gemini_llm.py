import os
import google.generativeai as genai
from langsmith import traceable
from dotenv import load_dotenv

# .env ファイルをロード
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Gemini APIの初期化
genai.configure(api_key=GEMINI_API_KEY)

# Geminiモデルの取得
gemini_model = genai.GenerativeModel("models/gemini-1.5-flash")


from agents.llm.base_llm import BaseLLM

# Geminiクライアント
class GeminiLLM(BaseLLM):

    def execute(self, system_prompts: list[str], user_prompts: list[str]):
        response = self.__execute(system_prompts=system_prompts, user_prompts=user_prompts)
        return response.text
    
    @traceable(name="Gemini + LangGraph run")
    def __execute(self, system_prompts: list[str], user_prompts: list[str]):
        return gemini_model.generate_content(system_prompts + user_prompts)
