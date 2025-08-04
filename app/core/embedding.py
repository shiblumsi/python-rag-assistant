from sentence_transformers import SentenceTransformer


# Load pre-trained sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Get embeddings for a list of text chunks
def get_embedding(text: str):
    try:
        embedding = model.encode(text)
        return embedding.tolist()
    except Exception as e:
        print("Embedding Error:", e)
        return None

# Get embeddings for a list of text chunks
def get_embeddings_for_chunks(chunks: list[str]):
    embeddings = []
    for chunk in chunks:
        emb = get_embedding(chunk)
        if emb:
            embeddings.append(emb)
    return embeddings
