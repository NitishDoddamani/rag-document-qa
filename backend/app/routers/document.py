from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.pdf_service import extract_text, chunk_text
from app.services.embedding_service import store_embeddings
import uuid

router = APIRouter(prefix="/documents", tags=["documents"])

ALLOWED_EXTENSIONS = ['.pdf', '.docx', '.doc']

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    
    filename = file.filename.lower()
    if not any(filename.endswith(ext) for ext in ALLOWED_EXTENSIONS):
        raise HTTPException(
            status_code=400,
            detail="Only PDF and Word documents (.pdf, .docx) are allowed"
        )
    
    file_bytes = await file.read()
    
    # Universal extraction
    text = extract_text(file_bytes, file.filename)
    
    if not text.strip():
        raise HTTPException(
            status_code=400,
            detail="Could not extract text from file. File may be image-only without OCR support."
        )
    
    chunks = chunk_text(text)
    
    if not chunks:
        raise HTTPException(status_code=400, detail="No chunks generated from document")
    
    doc_id = str(uuid.uuid4())
    num_chunks = store_embeddings(chunks, doc_id)
    
    return {
        "message": "Document uploaded successfully",
        "doc_id": doc_id,
        "num_chunks": num_chunks,
        "filename": file.filename,
        "file_type": "PDF" if filename.endswith('.pdf') else "Word Document"
    }