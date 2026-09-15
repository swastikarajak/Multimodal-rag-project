from fastapi import FastAPI
from pydantic import BaseModel

from src.rag_pipeline import answer_question


# Create FastAPI application
app = FastAPI(
    title="Multimodal RAG API",
    description="Backend API for the Multimodal RAG system",
    version="1.0.0"
)


# -----------------------------
# Request model
# -----------------------------
class QuestionRequest(BaseModel):
    question: str


# -----------------------------
# Home / health-check endpoint
# -----------------------------
@app.get("/")
def home():
    return {
        "message": "Multimodal RAG API is running!"
    }


# -----------------------------
# Ask question endpoint
# -----------------------------
@app.post("/ask")
def ask_question(request: QuestionRequest):
    """
    Receive a question from the frontend
    and send it through the RAG pipeline.
    """

    result = answer_question(
        question=request.question,
        n_results=5
    )

    return result