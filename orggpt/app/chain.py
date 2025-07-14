from typing import List, Dict, Any
from .vectorstore import VectorStore
from .prompt import MEMO_SECTIONS, build_memo_prompt
from loguru import logger
import openai
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

class MemoRAGChain:
    """
    Retrieval-Augmented Generation chain for investment memos.
    """
    def __init__(self, vectorstore: VectorStore):
        self.vectorstore = vectorstore

    def generate_section(self, query: str, section: str, filters: Dict[str, Any] = None) -> str:
        """
        Retrieves relevant chunks and generates a memo section using OpenAI.
        """
        docs = self.vectorstore.query(query, n_results=8, filters=filters)
        context = "\n\n".join([d["content"] for d in docs])
        prompt = build_memo_prompt(context, section)
        logger.info(f"Generating section '{section}' with {len(docs)} context chunks.")
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=600
        )
        return response.choices[0].message.content.strip()

    def generate_memo(self, company_query: str, filters: Dict[str, Any] = None) -> Dict[str, str]:
        """
        Generates a full investment memo (all sections).
        """
        memo = {}
        for section in MEMO_SECTIONS:
            memo[section] = self.generate_section(company_query, section, filters)
        return memo 