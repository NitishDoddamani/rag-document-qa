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
    
    # Retrieve chunks with scores
    scored_chunks = search_similar_chunks(request.question)
    
    if not scored_chunks:
        return {
            "question": request.question,
            "answer": "No relevant content found in the document.",
            "chunks_used": 0,
            "citations": [],
            "hallucination_risk": "HIGH",
            "grounded": False
        }
    
    # Get answer
    result = get_answer(request.question, scored_chunks)
    
    # Build citations
    citations = [
        {
            "chunk_index": c["chunk_index"],
            "similarity_score": c["similarity"],
            "preview": c["text"][:150] + "..."
        }
        for c in scored_chunks[:3]  # Top 3 citations
    ]
    
    return {
        "question": request.question,
        "answer": result["answer"],
        "chunks_used": len(scored_chunks),
        "hallucination_risk": result["hallucination_risk"],
        "grounded": result["grounded"],
        "citations": citations
    }