import os
import google.generativeai as genai
from langsmith import traceable
from dotenv import load_dotenv
from llama_index.core.base.llms.types import ChatMessage, ChatResponse, MessageRole
from llama_index.core.base.llms.generic_utils import messages_to_prompt

from agents.integration.llm import CustomLLM

# .env ファイルをロード
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Gemini APIの初期化
genai.configure(api_key=GEMINI_API_KEY)

# Geminiモデルの取得
gemini_model = genai.GenerativeModel("models/gemini-1.5-flash")

# Geminiクライアント
class GeminiLLM(CustomLLM):

    def execute(self, system_prompts: list[str], user_prompts: list[str]):
        response = self.chat([ChatMessage(role=MessageRole.USER, content='\n'.join(system_prompts + user_prompts))])
        return response.message.content
    
    @traceable(name="Gemini")
    def chat(self, messages: list[ChatMessage], **kwargs) -> ChatResponse:
        prompt = messages_to_prompt(messages)
        response = gemini_model.generate_content(prompt)
        return ChatResponse(message=ChatMessage(role=MessageRole.ASSISTANT, content=response.text))
