from fastapi import FastAPI
from app.api import upload, query
from app.core.embedding_store import load_vector_store
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    load_vector_store()
    yield

app = FastAPI(title="Smart RAG API", lifespan=lifespan)

app.include_router(upload.router, prefix="/upload")
app.include_router(query.router, prefix="/query")

@app.get("/")
def root():
    return {"message": "RAG API is running 🚀"}
