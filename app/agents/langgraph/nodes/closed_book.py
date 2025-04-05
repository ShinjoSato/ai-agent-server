from agents.llm.gemini_llm import GeminiLLM as LLM


# LLMを使って質問に回答
def retrieve_information(inputs: dict) -> dict:
    state = inputs["state"]
    response = _retrieve_information(prompt=state["question"])
    print('OpenAI >>', response,)
    state["response"] = response
    return {"state": state}


def _retrieve_information(prompt: str) -> str:
    llm = LLM()
    response = llm.execute(
        system_prompts=[],
        user_prompts=[prompt]
    )
    return response
