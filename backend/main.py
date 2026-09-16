from pathlib import Path

from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel

from src.rag_pipeline import answer_question
from src.ingestion import process_document


# File types supported by our RAG system
ALLOWED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".png",
    ".jpg",
    ".jpeg"
}

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


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload a document and process it through
    the existing ingestion pipeline.
    """

          # Check whether a filename was provided
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No filename provided."
        )

    # Get only the filename, without any folder path
    safe_filename = Path(file.filename).name

    # Get file extension
    extension = Path(safe_filename).suffix.lower()

    # Check whether the file type is supported
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported file type. "
                "Allowed formats: PDF, DOCX, PNG, JPG, JPEG."
            )
        )

    # Save uploaded file inside data/uploads
    upload_directory = Path("data/uploads")
    upload_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    file_path = upload_directory / file.filename

    # Write uploaded file to disk
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # Process the uploaded document
    document, chunks = process_document(
        str(file_path)
    )

    return {
        "message": "File uploaded and processed successfully!",
        "filename": file.filename,
        "chunks_created": len(chunks)
    }