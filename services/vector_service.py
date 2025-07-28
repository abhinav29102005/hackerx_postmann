# services/vector_service.py
import logging
import uuid
from typing import List
from openai import OpenAI
from pinecone import Pinecone, ServerlessSpec
from config import settings

# --- Initialize Clients ---
openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
pinecone_client = Pinecone(api_key=settings.PINECONE_API_KEY)

def get_embeddings(texts: List[str]) -> List[List[float]]:
    """Generates embeddings for a list of text chunks."""
    logging.info(f"Generating embeddings for {len(texts)} chunks.")
    response = openai_client.embeddings.create(input=texts, model=settings.EMBEDDING_MODEL)
    return [item.embedding for item in response.data]

def setup_and_upsert_pinecone(chunks: List[str], embeddings: List[List[float]], namespace: str):
    """Sets up a Pinecone index and upserts the document chunks."""
    if settings.PINECONE_INDEX_NAME not in pinecone_client.list_indexes().names():
        logging.info(f"Creating new Pinecone index: {settings.PINECONE_INDEX_NAME}")
        pinecone_client.create_index(
            name=settings.PINECONE_INDEX_NAME,
            dimension=settings.EMBEDDING_DIMENSION,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )
    index = pinecone_client.Index(settings.PINECONE_INDEX_NAME)
    logging.info(f"Upserting {len(chunks)} vectors to namespace: {namespace}")
    vectors_to_upsert = [
        {"id": f"chunk_{i}", "values": emb, "metadata": {"text": chunk}}
        for i, (chunk, emb) in enumerate(zip(chunks, embeddings))
    ]
    for i in range(0, len(vectors_to_upsert), 100):
        batch = vectors_to_upsert[i:i + 100]
        index.upsert(vectors=batch, namespace=namespace)
    logging.info("Upsert complete.")
    return index

def query_pinecone(index, query: str, namespace: str, top_k: int = 3) -> str:
    """Queries Pinecone to retrieve relevant context for a question."""
    query_embedding = get_embeddings([query])[0]
    results = index.query(
        namespace=namespace,
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True
    )
    return "\n---\n".join([match['metadata']['text'] for match in results['matches']])

def cleanup_namespace(index, namespace: str):
    """Deletes all vectors in a given namespace to clean up."""
    logging.info(f"Cleaning up namespace: {namespace}")
    index.delete(delete_all=True, namespace=namespace)