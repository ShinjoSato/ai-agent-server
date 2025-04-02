from agents.llm.gemini_llm import GeminiLLM as LLM


# OpenAI APIを使って回答が十分かを判定
def route_workflow(inputs: dict) -> dict:
    state = inputs["state"]
    response = _route_workflow(prompts=[state['question'], state['openai_response']])
    state["need_search"] = "No" not in response
    next = "browse_web" if state["need_search"] else "summarize_with_openai"
    state["next"] = next
    return {"state": state, "next": next}

def _route_workflow(prompts: list[str]) -> str:
    llm = LLM()
    response = llm.execute(
        system_prompts=["以下の回答が十分か、それともインターネット検索が必要か判断してください。"],
        user_prompts=[f"質問: {prompts[0]}\n"
            f"回答: {prompts[1]}\n\n"
            "この回答で十分なら「NO」と答えてください。\n"
            "情報が不十分で検索が必要なら「YES」と答えてください。"
        ]
    )
    return response
