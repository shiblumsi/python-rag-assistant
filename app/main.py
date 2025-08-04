from fastapi import FastAPI
from app.api import upload, query

from contextlib import asynccontextmanager
from app.core.vector_store import load_faiss_index


@asynccontextmanager
async def lifespan(app: FastAPI):
    #Load FAISS index and metadata during startup
    load_faiss_index()
    yield

app = FastAPI(title="RAG API", lifespan=lifespan)

# Register API routes
app.include_router(upload.router, prefix="/upload")
app.include_router(query.router, prefix="/query")

@app.get("/")
def root():
    return {"message": "RAG API is running 🚀"}
