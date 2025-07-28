# main.py

from fastapi import FastAPI
# Corrected import: No 'hackrx_app' prefix
from api import router as api_router

# Initialize the FastAPI application
app = FastAPI(
    title="Intelligent Query–Retrieval System",
    description="API for HackRx: Processes policy documents and answers questions.",
    version="1.0.0"
)

# Include the API router
app.include_router(api_router.router)

# Optional: Add a root endpoint for simple health checks
@app.get("/", include_in_schema=False)
async def root():
    return {"message": "Query-Retrieval System is running. See /docs for API documentation."}