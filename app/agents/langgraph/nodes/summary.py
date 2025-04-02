from agents.llm.gemini_llm import GeminiLLM as LLM
from utils.file_handle import load_prompt


# OpenAI APIで最終的な回答を要約
def summarize(inputs: dict) -> dict:
    state = inputs["state"]
    content_to_summarize = state["openai_response"]
    if state["need_search"]:
        content_to_summarize += "\n" + state["perplexity_response"]
    content_to_summarize = state["perplexity_response"] if state["need_search"] else state["openai_response"]

    response = _summarize(prompt=f"{content_to_summarize}")
    state["final_summary"] = response
    print('要約 >>', response,)
    return {"state": state}


def _summarize(prompt: str) -> str:
    llm = LLM()
    character_prompt = load_prompt("prompts/hattori.md")
    response = llm.execute(
        system_prompts=[character_prompt, "50トークン以内で要約してください"],
        user_prompts=[prompt]
    )
    return response
