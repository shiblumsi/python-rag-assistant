from fastapi import APIRouter, UploadFile, File, HTTPException
import os
from uuid import uuid4

from app.core.file_parser import extract_text
from app.utils.chunking import chunk_text
from app.core.embedding import get_embeddings_for_chunks
from app.core.vector_store import add_to_faiss, clear_faiss_index

router = APIRouter()

UPLOAD_DIR = "sample_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    filename = f"{uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    try:
        with open(file_path, "wb") as f:
            f.write(await file.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")

    try:
        # Extract text and split into chunks
        text = extract_text(file_path)
        chunks = chunk_text(text)
        embeddings = get_embeddings_for_chunks(chunks)   # Generate embeddings for each chunk
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed during text extraction or embedding: {str(e)}")

    metadatas = [{"chunk": i, "text": chunk, "source_file": filename} for i, chunk in enumerate(chunks)]


    clear_faiss_index()
    #Store in FAISS vector store
    add_to_faiss(embeddings, metadatas)

    return {
        "message": "Uploaded and indexed",
        "total_chunks": len(chunks),
        "source_file": file.filename
    }
