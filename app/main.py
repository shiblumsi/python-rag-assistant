from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.api import upload, query
from app.core.vector_store import load_faiss_index


@asynccontextmanager
async def lifespan(app: FastAPI):
    #Load FAISS index and metadata during startup
    load_faiss_index()
    yield

app = FastAPI(title="RAG API", lifespan=lifespan)


# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://python-rag-ui.streamlit.app"  # Deployed Streamlit UI
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routes
app.include_router(upload.router, prefix="/upload")
app.include_router(query.router, prefix="/query")

@app.get("/")
def root():
    return {"message": "RAG API is running 🚀"}
