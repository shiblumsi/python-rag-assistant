from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text: str):
    try:
        embedding = model.encode(text)
        return embedding.tolist()
    except Exception as e:
        print("Embedding Error:", e)
        return None

def get_embeddings_for_chunks(chunks: list[str]):
    return [get_embedding(chunk) for chunk in chunks if get_embedding(chunk)]
