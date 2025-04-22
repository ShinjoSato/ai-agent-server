from agents.integration.gemini_llm import GeminiLLM
from agents.integration.qdrant_database import QdrantDB
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext


if __name__ == '__main__':
    documents = SimpleDirectoryReader("./knowledge").load_data()
    llm = GeminiLLM()

    qdrant_db = QdrantDB()
    vector_store = qdrant_db.get_store()

    # ストレージコンテキストを作成
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
        llm=llm
    )
    print('アップロード完了しました')
