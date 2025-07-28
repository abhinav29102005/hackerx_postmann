# services/llm_service.py
import logging
from openai import OpenAI
from config import settings

# --- Initialize Client ---
openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)

def get_answer(question: str, context: str) -> str:
    """Uses the LLM to generate a concise answer based on the retrieved context."""
    logging.info(f"Generating LLM answer for question: '{question[:50]}...'")
    prompt = (
        "You are an expert Q&A system for policy documents. "
        "Based ONLY on the provided context below, answer the user's question accurately and concisely. "
        "Do not use any outside knowledge. If the answer is not in the context, state that clearly.\n\n"
        f"CONTEXT:\n{context}\n\n"
        f"QUESTION: {question}\n\n"
        "ANSWER:"
    )
    response = openai_client.chat.completions.create(
        model=settings.LLM_MODEL,
        messages=[{"role": "system", "content": prompt}],
        temperature=0.0,
        max_tokens=200,
    )
    return response.choices[0].message.content.strip()