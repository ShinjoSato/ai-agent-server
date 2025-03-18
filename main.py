import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph

# .env ファイルをロード
load_dotenv()

# APIキーを環境変数から取得
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

# システムの状態を管理するクラス
class QAState:
    def __init__(self, question: str):
        self.question = question
        self.openai_response = None
        self.need_search = None
        self.perplexity_response = None
        self.final_summary = None
        self.audio_url = None
        self.next = None

def end_node(inputs: dict) -> dict:
    state = inputs["state"]
    return {"state": state}

from clients.openai_client import answer_with_openai, check_response_quality, summarize_with_openai
from clients.perplexity_client import search_with_perplexity
from clients.elevenlabs_client import generate_speech

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
graph = workflow.compile()
# print(graph.get_graph())
# print(graph.get_graph().draw_ascii())


# ワークフローの実行
def run_workflow(question: str):
    state = QAState(question).__dict__  # ✅ `dict` に変換
    result = graph.invoke({"state": state})  # ✅ `state` を `dict` にして渡す
    return result["state"]["audio_url"]  # ✅ `dict` から `audio_url` を取得

# 実行例
if __name__ == "__main__":
    question = "東京で桜はいつ頃から咲きますか？"
    print('ユーザー >>', question)
    audio_output = run_workflow(question)
