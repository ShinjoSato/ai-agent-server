from langgraph.graph import StateGraph

from .nodes.openai_client import answer_with_openai, check_response_quality, summarize_with_openai
from .nodes.perplexity_client import search_with_perplexity
from .nodes.elevenlabs_client import generate_speech

def create_graph():
    # LangGraphでワークフローを構築
    workflow = StateGraph(dict)  # ✅ `dict` を状態として使う

    workflow.add_node("answer_with_openai", answer_with_openai)
    workflow.add_node("check_response_quality", check_response_quality)
    workflow.add_node("search_with_perplexity", search_with_perplexity)
    workflow.add_node("summarize_with_openai", summarize_with_openai)
    workflow.add_node("generate_speech", generate_speech)
    workflow.add_node("end_node", end_node)


    workflow.set_entry_point("answer_with_openai")
    workflow.add_edge("answer_with_openai", "check_response_quality")
    workflow.add_conditional_edges(
        "check_response_quality",
        lambda state: state["next"], {
            "search_with_perplexity": "search_with_perplexity",
            "summarize_with_openai": "summarize_with_openai"
        }
    )
    workflow.add_edge("search_with_perplexity", "summarize_with_openai")
    workflow.add_edge("summarize_with_openai", "generate_speech")
    workflow.add_edge( "generate_speech", "end_node")
    workflow.set_finish_point("end_node")

    # ワークフローのコンパイル
    return workflow.compile()
    # print(graph.get_graph())
    # print(graph.get_graph().draw_ascii())

def end_node(inputs: dict) -> dict:
    state = inputs["state"]
    return {"state": state}
