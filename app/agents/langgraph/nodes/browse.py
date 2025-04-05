# from agents.llm.perplexity_llm import PerplexityLLM as LLM
from agents.llm.tavily_llm import TavilyLLM as LLM


# LLMを使って検索
def browse_web(inputs: dict) -> dict:
    state = inputs["state"]
    response = _browse_with_llm(prompt=state["question"])
    print('Perplexity >>', response,)
    state["response"] = response
    return {"state": state}


def _browse_with_llm(prompt: str) -> str:
    llm = LLM()
    response = llm.execute(
        system_prompts=[],
        user_prompts=[prompt]
    )
    return response
