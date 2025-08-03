from fastapi import APIRouter
from pydantic import BaseModel
from app.core.embedding import get_embedding
from app.core.ocr import extract_text_from_base64
from app.core.vector_store import search_similar_vectors
from app.core.llm import ask_llm

router = APIRouter()

class QueryRequest(BaseModel):
    question: str
    image_base64: str = None  


@router.post("/")
def query_rag(request: QueryRequest):
    question = request.question

    if request.image_base64:
        try:
            image_text = extract_text_from_base64(request.image_base64)
            question += f"\n\nImage Text:\n{image_text}"
        except Exception as e:
            print("OCR error:", e)

    query_vector = get_embedding(question)
    if not query_vector:
        return {"error": "Failed to create embedding."}

    try:
        results = search_similar_vectors(query_vector, top_k=3)
    except ValueError as e:
        return {"error": str(e)}

    if not results:
        return {
            "question": question,
            "answer": "Sorry, no relevant information found.",
            "context_snippet": "",
            "sources": [],
            "error": None,
        }


    unique_sources = []
    seen = set()
    for r in results:
        key = (r["source_file"], r["chunk"])
        if key not in seen:
            unique_sources.append({"file": r["source_file"], "chunk": r["chunk"]})
            seen.add(key)


    full_context = "\n\n".join([r['text'] for r in results])
    context_snippet = full_context[:300].replace("\n", " ").strip() + ("..." if len(full_context) > 300 else "")

    answer = ask_llm(full_context, question)

    if "Error" in answer or "404" in answer:
        answer = "Sorry, I couldn't find a relevant answer to your question."

    return {
        "question": question,
        "answer": answer,
        "context_snippet": context_snippet,
        "sources": unique_sources,
        "error": None,
    }
