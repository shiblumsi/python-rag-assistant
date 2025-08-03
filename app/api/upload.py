from fastapi import APIRouter, UploadFile, File
import os
from uuid import uuid4


from app.core.file_parser import extract_text
from app.utils.chunking import chunk_text
from app.core.embedding import get_embeddings_for_chunks
from app.core.vector_store import add_to_faiss

router = APIRouter()

UPLOAD_DIR = "sample_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    filename = f"{uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())


    text = extract_text(file_path)
    chunks = chunk_text(text)
    embeddings = get_embeddings_for_chunks(chunks)

    print("Embeddings:", embeddings)
    print("Total Chunks:", len(chunks))



    metadatas = [{"chunk": i, "text": chunk, "source_file": file.filename} for i, chunk in enumerate(chunks)]


    add_to_faiss(embeddings, metadatas)

    return {
        "message": "Uploaded and indexed",
        "total_chunks": len(chunks),
        "source_file": file.filename
    }
