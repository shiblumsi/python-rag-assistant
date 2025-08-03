import faiss
import numpy as np
import os
import pickle

VECTOR_SIZE = 384
INDEX_FILE = "vector_store/index.faiss"
META_FILE = "vector_store/index_meta.pkl"

faiss_index = None
faiss_metadata = []

def load_faiss_index():
    global faiss_index, faiss_metadata

    if os.path.exists(INDEX_FILE):
        faiss_index = faiss.read_index(INDEX_FILE)
        print("FAISS index loaded")
    else:
        faiss_index = faiss.IndexFlatL2(VECTOR_SIZE)
        print(" New FAISS index created")

    if os.path.exists(META_FILE):
        with open(META_FILE, "rb") as f:
            faiss_metadata = pickle.load(f)
            print(f" Loaded {len(faiss_metadata)} metadata entries")
    else:
        faiss_metadata = []
        print("ℹ No metadata found")

def save_faiss_index():
    global faiss_index, faiss_metadata

    os.makedirs(os.path.dirname(INDEX_FILE), exist_ok=True)

    faiss.write_index(faiss_index, INDEX_FILE)
    with open(META_FILE, "wb") as f:
        pickle.dump(faiss_metadata, f)
    print(" FAISS index and metadata saved")

def add_to_faiss(embeddings, metadatas):
    global faiss_index, faiss_metadata

    vectors = np.array(embeddings).astype("float32")
    if vectors.ndim == 1:
        vectors = np.expand_dims(vectors, axis=0)

    if vectors.shape[1] != faiss_index.d:
        raise ValueError(f"Embedding dim {vectors.shape[1]} ≠ FAISS index dim {faiss_index.d}")

    faiss_index.add(vectors)
    faiss_metadata.extend(metadatas)
    save_faiss_index()

def search_similar_vectors(query_vector, top_k=5):
    global faiss_index, faiss_metadata

    if faiss_index is None or faiss_index.ntotal == 0:
        raise ValueError(" FAISS index not loaded or empty")

    query_vector = np.array([query_vector]).astype("float32")
    D, I = faiss_index.search(query_vector, top_k)
    results = []

    for i in I[0]:
        if i < len(faiss_metadata):
            results.append(faiss_metadata[i])
        else:
            results.append({
                "text": "[Missing]",
                "source_file": "unknown",
                "chunk": -1
            })

    return results
