import ollama

def get_answer(question: str, context_chunks: list) -> str:
    context = "\n\n".join(context_chunks)
    
    prompt = f"""You are a helpful assistant. Answer the question based ONLY on the provided context below.
If the answer is not found in the context, say "I couldn't find relevant information in the document."

Context:
{context}

Question: {question}

Answer:"""
    
    response = ollama.chat(
        model='llama3.2:1b',
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response['message']['content']