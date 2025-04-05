from agents.integration.tavily_search import TavilyLLM
from agents.integration.gemini_llm import GeminiLLM


"""
ネット検索で最新の情報を取得する。
"""
def surf_internet(prompt: str) -> str:
    llm = TavilyLLM()
    response = llm.execute(
        system_prompts=[],
        user_prompts=[prompt]
    )
    return response


"""
ユーザーの質問の答えを取得する。
"""
def ask_question(user_prompt: str, system_prompts: list[str]=[]) -> str:
    llm = GeminiLLM()
    response = llm.execute(
        system_prompts=system_prompts,
        user_prompts=[user_prompt]
    )
    return response
