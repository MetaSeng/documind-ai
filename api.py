import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from src.rag_pipeline import ingest_document, answer_question

app = FastAPI(
    title="DocuMind AI API",
    description="Upload PDF documents and ask questions using RAG.",
    version="1.0.0",
)

UPLOAD_DIR = "data"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ── 1. Health Check ──────────────────────────────────────────
@app.get("/health")
def health_check():
    """
    Returns a simple status message to confirm the API is running.
    """
    return {"status": "ok", "message": "DocuMind AI API is running!"}


# ── 2. Ingest PDF ────────────────────────────────────────────
@app.post("/ingest")
async def ingest_pdf(file: UploadFile = File(...)):
    """
    Accepts a PDF file upload, saves it to the data/ folder,
    and runs the full ingestion pipeline (load → split → embed → store).
    """
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    # Save the uploaded file to data/
    save_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Run ingestion pipeline
    try:
        ingest_document(save_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")

    return {
        "status": "success",
        "message": f"'{file.filename}' has been ingested successfully.",
        "saved_to": save_path,
    }


# ── 3. Ask a Question ────────────────────────────────────────
class QuestionRequest(BaseModel):
    question: str
    top_k: int = 3


@app.post("/ask")
def ask_question(request: QuestionRequest):
    """
    Accepts a question string and returns an AI-generated answer
    based on the documents stored in ChromaDB.
    """
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    try:
        answer = answer_question(request.question, top_k=request.top_k)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")

    return {
        "question": request.question,
        "answer": answer,
    }
