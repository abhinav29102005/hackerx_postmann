# api/router.py

import logging
import uuid
from fastapi import APIRouter, Depends, HTTPException, status, Header

from schemas import HackRxRequest, HackRxResponse
from config import settings
# Import the new, separated services
from services import document_service, vector_service, llm_service

# Create an API router
router = APIRouter(prefix="/api/v1", tags=["Query System"])

# --- Security Dependency ---
async def verify_token(authorization: str = Header(...)):
    # ... (this function remains the same)
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authentication scheme.")
    token = authorization.split(" ")[1]
    if token != settings.AUTH_BEARER_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token.")

# --- API Endpoint ---
@router.post(
    "/hackrx/run",
    response_model=HackRxResponse,
    dependencies=[Depends(verify_token)]
)
async def run_submission(request: HackRxRequest):
    """
    Main API endpoint that orchestrates the RAG pipeline by calling services.
    """
    try:
        # 1. Document Processing
        document_text = document_service.get_text_from_pdf_url(str(request.documents))
        text_chunks = document_service.chunk_text(document_text)

        # 2. Vectorization and Storage
        chunk_embeddings = vector_service.get_embeddings(text_chunks)
        namespace = f"req-{uuid.uuid4()}"
        index = vector_service.setup_and_upsert_pinecone(text_chunks, chunk_embeddings, namespace)

        # 3. Answering Questions
        answers = []
        for question in request.questions:
            context = vector_service.query_pinecone(index, question, namespace)
            answer = llm_service.get_answer(question, context)
            answers.append(answer)

        # 4. Cleanup
        vector_service.cleanup_namespace(index, namespace)

        return HackRxResponse(answers=answers)
    
    except Exception as e:
        logging.error(f"An unexpected error occurred in the submission endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))