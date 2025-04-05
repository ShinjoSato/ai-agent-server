from agents.llm.gemini_llm import GeminiLLM as LLM
from utils.file_handle import load_prompt


# OpenAI APIで最終的な回答を要約
def summarize(inputs: dict) -> dict:
    state = inputs["state"]
    content_to_summarize = state["response"]
    content_to_summarize = state["response"]

    response = _summarize(prompt=f"{content_to_summarize}")
    state["summary"] = response
    print('要約 >>', response,)
    return {"state": state}


def _summarize(prompt: str) -> str:
    llm = LLM()
    character_prompt = load_prompt("prompts/hattori.md")
    response = llm.execute(
        system_prompts=[character_prompt],
        user_prompts=[f"以下の文章を50トークン以内で要約して音声合成用のひらがなに変換してください。\n\n文章:\n{prompt}"]
    )
    return response
