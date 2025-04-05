from utils.file_handle import load_prompt
from utils.generative_ai_util import ask_question


# OpenAI APIで最終的な回答を要約
def summarize(inputs: dict) -> dict:
    state = inputs["state"]
    content_to_summarize = state["response"]

    # response = _summarize(prompt=f"{content_to_summarize}")
    character_prompt = load_prompt("prompts/hattori.md")
    response = ask_question(
        user_prompt=f"以下の文章を50トークン以内で要約して音声合成用のひらがなに変換してください。\n\n文章:\n{content_to_summarize}",
        system_prompts=[character_prompt]
    )
    state["summary"] = response
    print('要約 >>', response,)
    return {"state": state}
