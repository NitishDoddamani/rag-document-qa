from sentence_transformers import SentenceTransformer
import chromadb
from app.config import CHROMA_PERSIST_DIR

model = SentenceTransformer('models/all-MiniLM-L6-v2')

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
        ids=ids
    )
    
    return len(chunks)

def search_similar_chunks(query: str, n_results: int = 5) -> list:
    collection = get_or_create_collection("documents")
    
    query_embedding = model.encode([query]).tolist()
    
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=n_results
    )
    
    return results['documents'][0]