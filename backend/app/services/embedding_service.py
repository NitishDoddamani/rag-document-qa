from sentence_transformers import SentenceTransformer
import chromadb
from app.config import CHROMA_PERSIST_DIR

model = SentenceTransformer('all-MiniLM-L6-v2')
chroma_client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)

def get_or_create_collection(collection_name: str):
    return chroma_client.get_or_create_collection(name=collection_name)

def store_embeddings(chunks: list, doc_id: str):
    collection = get_or_create_collection("documents")
    embeddings = model.encode(chunks).tolist()
    ids = [f"{doc_id}_chunk_{i}" for i in range(len(chunks))]
    
    collection.add(
        embeddings=embeddings,
        documents=chunks,
        ids=ids,
        metadatas=[{"doc_id": doc_id, "chunk_index": i} for i in range(len(chunks))]
    )
    return len(chunks)

def search_similar_chunks(query: str, n_results: int = 10):
    collection = get_or_create_collection("documents")
    query_embedding = model.encode([query]).tolist()
    
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=n_results,
        include=["documents", "distances", "metadatas"]
    )
    
    chunks = results['documents'][0]
    distances = results['distances'][0]
    metadatas = results['metadatas'][0]
    
    # Convert distance to similarity score (0 to 1)
    scored_chunks = []
    for chunk, distance, meta in zip(chunks, distances, metadatas):
        similarity = round(1 - distance, 4)
        scored_chunks.append({
            "text": chunk,
            "similarity": similarity,
            "chunk_index": meta.get("chunk_index"),
            "doc_id": meta.get("doc_id")
        })
    
    # Filter low quality chunks — only keep similarity > 0.3
    scored_chunks = [c for c in scored_chunks if c["similarity"] > 0.1]
    
    # Sort by similarity
    scored_chunks.sort(key=lambda x: x["similarity"], reverse=True)
    
    return scored_chunks