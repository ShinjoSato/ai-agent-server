from agents.integration.tavily_search import TavilyLLM
from agents.integration.gemini_llm import GeminiLLM
from agents.integration.qdrant_database import QdrantDB
from llama_index.core import VectorStoreIndex
from langsmith import traceable


"""
ネット検索で最新の情報を取得する。
"""
def surf_internet(prompt: str) -> str:
    llm = TavilyLLM()
    response = llm.execute(
        system_prompts=[],
        user_prompts=[prompt]
    )
    return response


"""
ユーザーの質問の答えを取得する。
"""
def ask_question(user_prompt: str, system_prompts: list[str]=[]) -> str:
    llm = GeminiLLM()
    response = llm.execute(
        system_prompts=system_prompts,
        user_prompts=[user_prompt]
    )
    return response


def retrieval_augmented_generation(user_prompt: str) -> str:
    """
    RAG (Retrieval-Augmented Generation)を使った検索をする。
    """
    # LLMをGeminiに設定してインデックス作成
    llm = GeminiLLM()
    index =  convert_documents_into_index(llm=llm)

    # クエリ実行
    query_engine = index.as_query_engine()
    response = query_engine.query(user_prompt)
    return response


@traceable(name="vector-store-index")
def convert_documents_into_index(llm):
    """
    ドキュメントをベクトル化
    """
    qdrant_db = QdrantDB()
    vector_store = qdrant_db.get_store()
    return VectorStoreIndex.from_vector_store(vector_store=vector_store, llm=llm)
