from langgraph.graph import StateGraph
from agents.integration.elevenlabs_tts import ElevenLabs
from utils.file_handle import load_prompt
from utils.generative_ai_util import ask_question, surf_internet, retrieval_augmented_generation


def _get_workflow():
    # LangGraphでワークフローを構築
    workflow = StateGraph(dict)  # ✅ `dict` を状態として使う

    workflow.add_node("route_workflow", route_workflow)
    workflow.add_node("retrieve_information", retrieve_information)
    workflow.add_node("browse_web", browse_web)
    workflow.add_node("summarize", summarize)
    workflow.add_node("generate_speech", generate_speech)
    workflow.add_node("end_node", end_node)


    workflow.set_entry_point("route_workflow")
    workflow.add_conditional_edges(
        "route_workflow",
        lambda state: state["next"], {
            "1": "retrieve_information",
            "2": "browse_web"
        }
    )
    workflow.add_edge("retrieve_information", "summarize")
    workflow.add_edge("browse_web", "summarize")
    workflow.add_edge("summarize", "generate_speech")
    workflow.add_edge( "generate_speech", "end_node")
    workflow.set_finish_point("end_node")

    # ワークフローのコンパイル
    return workflow


"""
質問内容によって使用するLLMを選別。
"""
def route_workflow(inputs: dict) -> dict:
    state = inputs["state"]

    system_prompts = [
        """
        貴方は優秀なAIのエキスパートです。
        ユーザーの質問内容を理解し、質問を答えるのに最も適したAIを数字で教えてください。
        数字のみ答えてください。
        Geminiの場合は「1」と答えてください。
        Tavilyの場合は「2」と答えてください。
        答えがわからない場合は「1」と答えてください。
        Tavilyはリアルタイムで情報を取得できます。
        """
    ]
    response = ask_question(user_prompt=state['question'], system_prompts=system_prompts)

    state["select_ai"] = response.strip() 
    next = state["select_ai"]
    state["next"] = next
    return {"state": state, "next": next}


"""
RAGを使って質問に回答
"""
def retrieve_information(inputs: dict) -> dict:
    state = inputs["state"]
    response = retrieval_augmented_generation(user_prompt=state["question"])
    print('OpenAI >>', response,)
    state["response"] = response
    return {"state": state}


"""
LLMを使ってネット検索
"""
def browse_web(inputs: dict) -> dict:
    state = inputs["state"]
    response = surf_internet(prompt=state["question"])
    print('Perplexity >>', response,)
    state["response"] = response
    return {"state": state}


"""
回答を要約
"""
def summarize(inputs: dict) -> dict:
    state = inputs["state"]
    content_to_summarize = state["response"]

    character_prompt = load_prompt("prompts/hattori.md")
    response = ask_question(
        user_prompt=f"以下の文章を50トークン以内で要約して音声合成用のひらがなに変換してください。\n\n文章:\n{content_to_summarize}",
        system_prompts=[character_prompt]
    )
    state["summary"] = response
    print('要約 >>', response,)
    return {"state": state}


"""
テキストを音声化
"""
def generate_speech(inputs: dict) -> dict:
    state = inputs["state"]
    elvnlbs = ElevenLabs()
    elvnlbs.execute(user_prompts=state["summary"])
    return {"state": state}


def create_graph():
    workflow = _get_workflow()
    graph = workflow.compile()
    print(graph.get_graph().draw_ascii())
    return graph

def end_node(inputs: dict) -> dict:
    state = inputs["state"]
    return {"state": state}
