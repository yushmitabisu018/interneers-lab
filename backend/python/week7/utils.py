from sentence_transformers import SentenceTransformer
import numpy as np

_model = None

def get_default_model():
    global _model
    if _model is None:
       _model = SentenceTransformer('all-MiniLM-L6-v2')
    return _model

def cosine_similarity(vec_a, vec_b):
    dot_product= np.dot(vec_a, vec_b)
    norm_a= np.linalg.norm(vec_a)
    norm_b= np.linalg.norm(vec_b)
    if norm_a==0 or norm_b==0:
        return 0.0

    return dot_product/ (norm_a*norm_b)

def semantic_search(query, texts=None, ids=None, model=None, embeddings=None, top_k=5, threshold=0.0):
    model = model or get_default_model()

    if embeddings is None:
        if texts is None:
            raise ValueError("texts must be provided when embeddings is None")
        embeddings = model.encode(texts)

    query_embedding = model.encode([query])[0]

    similarities = []
    for i, emb in enumerate(embeddings):
        sim = cosine_similarity(query_embedding, emb)
        if sim >= threshold:
            item_id= ids[i] if ids else (texts[i] if texts is not None else i)
            similarities.append((item_id, sim))

    similarities.sort(key=lambda x: x[1], reverse=True)
    return similarities[:top_k]


def semantic_search_ids(query, texts=None, ids=None, model=None, embeddings=None, top_k=5, threshold=0.0):
    results = semantic_search(query, texts=texts, ids=ids, model=model, embeddings=embeddings, top_k=top_k, threshold=threshold)
    return [item_id for item_id, _ in results]