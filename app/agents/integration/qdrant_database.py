import os
from dotenv import load_dotenv
# from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.vector_stores.qdrant import QdrantVectorStore

# .env ファイルをロード
load_dotenv()
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_API_URL = os.getenv("QDRANT_API_URL")

client = QdrantClient(
    url=QDRANT_API_URL,
    api_key=QDRANT_API_KEY
)


class QdrantDB():
    def recreate_collection(self, collection_name: str):
        client.recreate_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
        )
    
    def get_store(self):
        try:
            # 初回はコレクションを登録
            client.get_collection("ai-agent-server-rag")
        except Exception as e:
            # 初回以降は更新
            client.recreate_collection(
                collection_name="ai-agent-server-rag",
                vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
            )

        return QdrantVectorStore(
            collection_name="ai-agent-server-rag",
            client=client,
        )
