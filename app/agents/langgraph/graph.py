from langgraph.graph import StateGraph

from .nodes.browse import browse_web
from .nodes.closed_book import retrieve_information
from .nodes.route import route_workflow
from .nodes.summary import summarize
from .nodes.elevenlabs_client import generate_speech

def create_graph():
    # LangGraphでワークフローを構築
    workflow = StateGraph(dict)  # ✅ `dict` を状態として使う

    workflow.add_node("retrieve_information", retrieve_information)
    workflow.add_node("route_workflow", route_workflow)
    workflow.add_node("browse_web", browse_web)
    workflow.add_node("summarize", summarize)
    workflow.add_node("generate_speech", generate_speech)
    workflow.add_node("end_node", end_node)


    workflow.set_entry_point("retrieve_information")
    workflow.add_edge("retrieve_information", "route_workflow")
    workflow.add_conditional_edges(
        "route_workflow",
        lambda state: state["next"], {
            "browse_web": "browse_web",
            "summarize": "summarize"
        }
    )
    workflow.add_edge("browse_web", "summarize")
    workflow.add_edge("summarize", "generate_speech")
    workflow.add_edge( "generate_speech", "end_node")
    workflow.set_finish_point("end_node")

    # ワークフローのコンパイル
    return workflow.compile()
    # print(graph.get_graph())
    # print(graph.get_graph().draw_ascii())

def end_node(inputs: dict) -> dict:
    state = inputs["state"]
    return {"state": state}
