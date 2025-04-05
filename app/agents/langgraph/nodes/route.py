from agents.llm.gemini_llm import GeminiLLM as LLM


# OpenAI APIを使って回答が十分かを判定
def route_workflow(inputs: dict) -> dict:
    state = inputs["state"]
    response = _route_workflow(prompts=[state['question']])
    state["select_ai"] = response.strip() 
    next = state["select_ai"]
    state["next"] = next
    return {"state": state, "next": next}

def _route_workflow(prompts: list[str]) -> str:
    llm = LLM()
    response = llm.execute(
        system_prompts=[
            """
            貴方は優秀なAIのエキスパートです。
            ユーザーの質問内容を理解し、質問を答えるのに最も適したAIを数字で教えてください。
            数字のみ答えてください。
            Geminiの場合は「1」と答えてください。
            Tavilyの場合は「2」と答えてください。
            答えがわからない場合は「1」と答えてください。
            Tavilyはリアルタイムで情報を取得できます。
            """
        ],
        user_prompts=[prompts[0]]
    )
    return response
