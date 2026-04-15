from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

def cosine_similarity(vec_a, vec_b):
    dot_product= np.dot(vec_a, vec_b)
    norm_a= np.linalg.norm(vec_a)
    norm_b= np.linalg.norm(vec_b)
    if norm_a==0 or norm_b==0:
        return 0.0

    return dot_product/ (norm_a*norm_b)


def semantic_search(query, texts, ids=None, model=model, top_k=5, threshold=0.0, scores=True):
   
    embeddings = model.encode(texts)
    query_embedding = model.encode([query])[0]

    similarities = []

    for i, emb in enumerate(embeddings):
        sim = cosine_similarity(query_embedding, emb)

        if sim >= threshold:
            item_id = ids[i] if ids else texts[i]
            similarities.append((item_id, sim))

    similarities.sort(key=lambda x: x[1], reverse=True)

    if scores:
        return similarities[:top_k]
    else:
        return [item_id for item_id, _ in similarities[:top_k]]