from typing import List, Dict, Any
from chromadb import Client, Settings
from chromadb.utils import embedding_functions
from loguru import logger
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class VectorStore:
    """
    Handles embedding and vector storage using Chroma and OpenAI.
    """
    def __init__(self, persist_dir: str = "./chroma_db"):
        self.client = Client(Settings(persist_directory=persist_dir))
        self.collection = self.client.get_or_create_collection(
            name="orggpt_docs",
            embedding_function=embedding_functions.OpenAIEmbeddingFunction(
                api_key=OPENAI_API_KEY,
                model_name="text-embedding-3-small"
            )
        )
        logger.info("Initialized Chroma vector store.")

    def add_chunks(self, chunks: List[Dict[str, Any]], doc_id: str) -> None:
        """
        Adds document chunks to the vector store.
        """
        texts = [c["content"] for c in chunks]
        metadatas = [{"section": c.get("section", "Unknown"), "doc_id": doc_id} for c in chunks]
        ids = [f"{doc_id}_{i}" for i in range(len(chunks))]
        self.collection.add(documents=texts, metadatas=metadatas, ids=ids)
        self.client.persist()
        logger.info(f"Added {len(chunks)} chunks to vector store for doc_id={doc_id}.")

    def query(self, query: str, n_results: int = 8, filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Queries the vector store for relevant chunks.
        """
        results = self.collection.query(query_texts=[query], n_results=n_results, where=filters)
        docs = []
        for i in range(len(results["ids"][0])):
            docs.append({
                "id": results["ids"][0][i],
                "content": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i]
            })
        return docs 