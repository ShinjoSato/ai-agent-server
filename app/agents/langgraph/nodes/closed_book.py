from utils.generative_ai_util import ask_question


# LLMを使って質問に回答
def retrieve_information(inputs: dict) -> dict:
    state = inputs["state"]
    response = ask_question(user_prompt=state["question"])
    print('OpenAI >>', response,)
    state["response"] = response
    return {"state": state}
