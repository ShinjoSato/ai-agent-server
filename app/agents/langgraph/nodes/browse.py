from utils.generative_ai_util import surf_internet


# LLMを使って検索
def browse_web(inputs: dict) -> dict:
    state = inputs["state"]
    response = surf_internet(prompt=state["question"])
    print('Perplexity >>', response,)
    state["response"] = response
    return {"state": state}
