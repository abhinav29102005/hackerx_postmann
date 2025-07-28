# services/document_service.py
import logging
import requests
from pypdf import PdfReader
import tiktoken
from typing import List
from config import settings

def get_text_from_pdf_url(pdf_url: str) -> str:
    """Fetches a PDF from a URL and extracts its text content."""
    logging.info(f"Fetching PDF from {pdf_url}")
    response = requests.get(pdf_url)
    response.raise_for_status()
    with PdfReader(stream=requests.get(pdf_url, stream=True).raw) as reader:
        return "".join(page.extract_text() for page in reader.pages if page.extract_text())

def chunk_text(text: str) -> List[str]:
    """Splits text into chunks based on token count."""
    logging.info("Chunking text document.")
    tokenizer = tiktoken.get_encoding("cl100k_base")
    tokens = tokenizer.encode(text)
    chunks = []
    for i in range(0, len(tokens), settings.CHUNK_SIZE_TOKENS - settings.CHUNK_OVERLAP_TOKENS):
        chunk_tokens = tokens[i:i + settings.CHUNK_SIZE_TOKENS]
        chunks.append(tokenizer.decode(chunk_tokens))
    return chunks