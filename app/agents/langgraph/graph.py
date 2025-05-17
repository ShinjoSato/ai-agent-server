from langgraph.graph import StateGraph
from agents.integration.elevenlabs_tts import ElevenLabs
from utils.file_handle import load_prompt
from utils.generative_ai_util import ask_question, surf_internet, retrieval_augmented_generation
from utils.util import get_logger
from fastapi import WebSocket

from models.User import User
from models.Message import Message


def _get_workflow():
    # LangGraphでワークフローを構築
    workflow = StateGraph(dict)  # ✅ `dict` を状態として使う

    workflow.add_node("route_workflow", route_workflow)
    workflow.add_node("retrieve_information", retrieve_information)
    workflow.add_node("browse_web", browse_web)
    workflow.add_node("summarize", summarize)
    workflow.add_node("translate", translate)
    workflow.add_node("transliterate", transliterate)
    workflow.add_node("generate_speech", generate_speech)

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
    workflow.add_conditional_edges(
        "summarize",
        lambda state: state["is_japanese"], {
            True: "transliterate",
            False: "translate"
        }
    )
    workflow.add_edge("transliterate", "generate_speech")
    workflow.add_edge("translate", "generate_speech")
    workflow.set_finish_point( "generate_speech")

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
    get_logger().info(response)

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
    get_logger().info(f"OpenAI >> {response}")
    state["response"] = response
    return {"state": state}


"""
LLMを使ってネット検索
"""
def browse_web(inputs: dict) -> dict:
    state = inputs["state"]
    response = surf_internet(prompt=state["question"])
    get_logger().info(f"Perplexity >> {response}")
    state["response"] = response
    return {"state": state}


"""
回答を要約
"""
def summarize(inputs: dict) -> dict:
    state = inputs["state"]
    content_to_summarize = state["response"]
    question = state["question"]

    character_prompt = load_prompt("prompts/hattori.md")
    response = ask_question(
        user_prompt=f"以下の質問に対する回答を100トークン以内で要約してください。\n\n質問:\n{question}\n\n回答:\n{content_to_summarize}",
        system_prompts=[character_prompt]
    )
    state["summary"] = response
    get_logger().info(f"要約 >> {response}")
    is_japanese = state["language"] == "ja"
    return {"state": state, "is_japanese": is_japanese}


"""
翻訳する。
"""
async def translate(inputs: dict) -> dict:
    state = inputs["state"]
    websocket = state["websocket"]
    summary = state["summary"]
    language = state["language"]
    response = ask_question(
        user_prompt=f"以下の文章を指定された言語に翻訳してください。\n\n文章:\n{summary}\n\n言語:\n{language}",
        system_prompts=[]
    )
    state["answer"] = response
    get_logger().info(f"翻訳 >> {response}")

    message = Message(
        message=response,
        language=language,
        type=0, # トーク
        status=1, # end
        user=User(
            type=0,
            name='Bot',
            voice_url='https://example.com/voice.mp3'
        )
    )
    message_json = message.dict()
    message_json['user'] = message.user.dict()
    get_logger().info(message_json)
    await websocket.send_json(message_json)
    return {"state": state}


"""
漢字が含まれる文をひらがな化
"""
async def transliterate(inputs: dict) -> dict:
    state = inputs["state"]
    language = state["language"]
    websocket = state["websocket"]
    summary = state["summary"]
    response = ask_question(
        user_prompt=f"以下の文章をひらがなに変換してください。\n\n文章:\n{summary}",
        system_prompts=[]
    )
    state["answer"] = response
    get_logger().info(f"ひらがな >> {response}")

    message = Message(
        message=summary,
        language=language,
        type=0, # トーク
        status=1, # end
        user=User(
            type=0,
            name='Bot',
            voice_url='https://example.com/voice.mp3'
        )
    )
    message_json = message.dict()
    message_json['user'] = message.user.dict()
    get_logger().info(message_json)
    await websocket.send_json(message_json)
    return {"state": state}


"""
テキストを音声化
"""
def generate_speech(inputs: dict) -> dict:
    state = inputs["state"]
    elvnlbs = ElevenLabs()
    elvnlbs.execute(user_prompts=state["answer"])
    get_logger().info('成功')
    return {"state": state}


"""
システムの状態を管理するクラス
"""
class QAState:
    def __init__(self, question: str, language: str, websocket: WebSocket):
        self.language = language
        self.question = question
        self.websocket = websocket
        self.response = None
        self.summary = None
        self.audio_url = None
        self.next = None
        self.answer = None


"""
ワークフローの実行
"""
async def run_workflow(question: str, language: str, websocket: WebSocket):
    state = QAState(question=question, language=language, websocket=websocket).__dict__  # ✅ `dict` に変換
    graph = create_graph()
    result = await graph.ainvoke({"state": state})  # ✅ `state` を `dict` にして渡す
    return result["state"]  # ✅ `dict` から `audio_url` を取得


"""
ワークフローの作成
"""
def create_graph():
    workflow = _get_workflow()
    graph = workflow.compile()
    get_logger().debug(f"\n{graph.get_graph().draw_ascii()}")
    return graph
