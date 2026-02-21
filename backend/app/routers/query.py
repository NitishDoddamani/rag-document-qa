from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.embedding_service import search_similar_chunks
from app.services.llm_service import get_answer

router = APIRouter(prefix="/query", tags=["query"])

class QueryRequest(BaseModel):
    question: str

@router.post("/ask")
async def ask_question(request: QueryRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    relevant_chunks = search_similar_chunks(request.question)
    
    if not relevant_chunks:
        raise HTTPException(status_code=404, detail="No relevant content found")
    
    answer = get_answer(request.question, relevant_chunks)
    
    return {
        "question": request.question,
        "answer": answer,
        "chunks_used": len(relevant_chunks)
    }