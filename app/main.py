from fastapi import FastAPI

app = FastAPI(title="Smart RAG API")


@app.get("/")
def root():
    return {"message": "RAG API is running 🚀"}