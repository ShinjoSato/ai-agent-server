from agents.integration.tavily_search import TavilyLLM
from agents.integration.gemini_llm import GeminiLLM
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
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

    # データ読み込み（PDFを ./data に置く）
    documents = SimpleDirectoryReader("./knowledge").load_data()

    # LLMをGeminiに設定してインデックス作成
    llm = GeminiLLM()
    # index = VectorStoreIndex.from_documents(documents, llm=llm)
    index =  convert_documents_into_index(documents=documents, llm=llm)

    # クエリ実行
    query_engine = index.as_query_engine()
    response = query_engine.query(user_prompt)
    return response


@traceable(name="vector-store-index")
def convert_documents_into_index(documents, llm):
    """
    ドキュメントをベクトル化
    """
    return VectorStoreIndex.from_documents(documents, llm=llm)
