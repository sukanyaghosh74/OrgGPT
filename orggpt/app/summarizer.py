from typing import List
import openai
import os
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

def summarize_chunks(chunks: List[str], section: str) -> str:
    """
    Summarizes a list of text chunks into a single section summary using OpenAI.
    """
    logger.info(f"Summarizing {len(chunks)} chunks for section '{section}'.")
    prompt = f"""You are an expert analyst. Summarize the following context for the section '{section}':\n\n{chr(10).join(chunks)}\n\nBe concise and use bullet points where appropriate."""
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=400
    )
    return response.choices[0].message.content.strip() 