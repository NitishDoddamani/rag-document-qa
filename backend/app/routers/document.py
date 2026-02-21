from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.pdf_service import extract_text_from_pdf, chunk_text
from app.services.embedding_service import store_embeddings
import uuid

router = APIRouter(prefix="/documents", tags=["documents"])

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")
    
    file_bytes = await file.read()
    
    # Extract text from PDF
    text = extract_text_from_pdf(file_bytes)
    
    if not text.strip():
        raise HTTPException(status_code=400, detail="Could not extract text from PDF")
    
    # Chunk the text
    chunks = chunk_text(text)
    
    # Generate doc_id and store embeddings
    doc_id = str(uuid.uuid4())
    num_chunks = store_embeddings(chunks, doc_id)
    
    return {
        "message": "Document uploaded successfully",
        "doc_id": doc_id,
        "num_chunks": num_chunks,
        "filename": file.filename
    }