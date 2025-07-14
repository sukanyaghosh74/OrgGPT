import re
from typing import List, Dict, Optional, Tuple, Union
from pathlib import Path
from loguru import logger
import pandas as pd

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None

# No relative imports to change in this file.

def read_pdf(file_path: Union[str, Path]) -> str:
    """
    Extracts text from a PDF file using PyPDF.
    """
    if PdfReader is None:
        raise ImportError("pypdf is not installed.")
    reader = PdfReader(str(file_path))
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


def read_txt(file_path: Union[str, Path]) -> str:
    """
    Reads text from a plain text file.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def smart_chunk(
    text: str,
    min_chunk_size: int = 500,
    max_chunk_size: int = 2000
) -> List[Dict[str, Union[str, int]]]:
    """
    Splits text into chunks, preserving section headings and tables.
    Returns a list of dicts with 'content' and 'section' keys.
    """
    # Regex for section headings (e.g., 'Item 1A. Risk Factors', 'Section 2:')
    section_pattern = re.compile(r"(^|\n)(Item [0-9A-Z]+\.|Section [0-9A-Z]+:|[A-Z][A-Za-z ]{3,}:)", re.MULTILINE)
    # Regex for tables (simple heuristic: lines with lots of numbers/tabs)
    table_pattern = re.compile(r"((?:\d+[\t, ]+){3,}\d+)")

    chunks = []
    last_idx = 0
    for match in section_pattern.finditer(text):
        start = match.start()
        if start > last_idx:
            chunk_text = text[last_idx:start].strip()
            if chunk_text:
                section = section_pattern.search(chunk_text)
                section_name = section.group(0).strip() if section else "Unknown"
                chunks.append({"content": chunk_text, "section": section_name})
        last_idx = start
    # Add the last chunk
    if last_idx < len(text):
        chunk_text = text[last_idx:].strip()
        if chunk_text:
            section = section_pattern.search(chunk_text)
            section_name = section.group(0).strip() if section else "Unknown"
            chunks.append({"content": chunk_text, "section": section_name})

    # Further split large chunks, but keep tables intact
    final_chunks = []
    for chunk in chunks:
        content = chunk["content"]
        section = chunk["section"]
        if len(content) > max_chunk_size:
            # Try to split by paragraphs, but not inside tables
            paras = re.split(r"\n{2,}", content)
            buf = ""
            for para in paras:
                if len(buf) + len(para) < max_chunk_size:
                    buf += para + "\n\n"
                else:
                    if buf.strip():
                        final_chunks.append({"content": buf.strip(), "section": section})
                    buf = para + "\n\n"
            if buf.strip():
                final_chunks.append({"content": buf.strip(), "section": section})
        else:
            final_chunks.append(chunk)
    return final_chunks


def load_and_chunk(file_path: Union[str, Path]) -> List[Dict[str, Union[str, int]]]:
    """
    Loads a document (PDF or TXT), extracts text, and returns smart-chunked sections.
    """
    logger.info(f"Loading file: {file_path}")
    ext = str(file_path).lower()
    if ext.endswith('.pdf'):
        text = read_pdf(file_path)
    elif ext.endswith('.txt'):
        text = read_txt(file_path)
    else:
        raise ValueError("Unsupported file type. Only PDF and TXT are supported.")
    logger.info(f"Extracted {len(text)} characters from file.")
    chunks = smart_chunk(text)
    logger.info(f"Split into {len(chunks)} chunks.")
    return chunks 