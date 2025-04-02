from agents.llm.perplexity_llm import PerplexityLLM as LLM
from utils.file_handle import load_prompt


# LLMを使って検索
def browse_web(inputs: dict) -> dict:
    state = inputs["state"]
    response = _browse_with_llm(prompt=state["question"])
    print('Perplexity >>', response,)
    state["perplexity_response"] = response
    return {"state": state}


def _browse_with_llm(prompt: str) -> str:
    llm = LLM()
    character_prompt = load_prompt("prompts/hattori.md")
    response = llm.execute(
        system_prompts=[character_prompt],
        user_prompt=[prompt]
    )
    return response
