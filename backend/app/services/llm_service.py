import ollama

def get_answer(question: str, scored_chunks: list) -> dict:
    
    if not scored_chunks:
        return {
            "answer": "This question does not appear to be related to the uploaded document.",
            "hallucination_risk": "LOW",
            "grounded": False
        }

    # Block off-topic questions early using similarity score
    if scored_chunks[0]["similarity"] < 0.2:
        return {
            "answer": "This question does not appear to be related to the uploaded document. Please ask questions based on the document content.",
            "hallucination_risk": "LOW",
            "grounded": False
        }

    context_parts = []
    for i, chunk in enumerate(scored_chunks):
        context_parts.append(f"[CHUNK {i+1} | Score: {chunk['similarity']:.2f}]\n{chunk['text']}")
    
    context = "\n\n".join(context_parts)
    
    strict_prompt = f"""You are a STRICT document assistant. Follow ALL rules below WITHOUT EXCEPTION.

RULES:
- Answer ONLY using information EXPLICITLY present in the CONTEXT below.
- If the answer is not directly in the context, respond ONLY with: "NOT FOUND IN DOCUMENT"
- Do NOT use outside knowledge, infer, or guess anything.
- Do NOT make up facts, numbers, or formulas.

FORMATTING RULES (MANDATORY):
- Use ## for main topic headings
- Use ### for subtopic headings
- Use bullet points (- ) for listing properties, features, or examples
- Use **bold** for important terms or key values
- Keep paragraphs short and readable
- If comparing multiple things (like LAN vs MAN vs WAN), use a separate ## section for each
- If question is simple, just answer clearly without unnecessary headings

CONTEXT:
{context}

QUESTION: {question}

ANSWER (strictly from context, well formatted with headings and bullets where needed):"""

    response = ollama.chat(
        model='command-r7b',
        messages=[{"role": "user", "content": strict_prompt}]
    )
    
    answer = response['message']['content']
    
    not_found_phrases = ["not found", "not present", "not mentioned", "not explicitly", "not in the document"]
    grounded = not any(phrase in answer.lower() for phrase in not_found_phrases)
    
    risky_phrases = ["however", "can be inferred", "generally", "typically", "in machine learning"]
    hallucination_risk = "HIGH" if any(phrase in answer.lower() for phrase in risky_phrases) else "LOW"
    
    return {
        "answer": answer,
        "hallucination_risk": hallucination_risk,
        "grounded": grounded
    }