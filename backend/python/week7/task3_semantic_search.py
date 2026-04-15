from sentence_transformers import SentenceTransformer
import numpy as np
from week7.utils import semantic_search

model = SentenceTransformer('all-MiniLM-L6-v2')

products=[
    {"name": "Lego Castle", "description": "Building blocks toy for construction and creative assembly"},
    {"name": "Wooden Blocks", "description": "Wooden building blocks for construction play for kids"},
    {"name": "Action Figure", "description": "Superhero action figure for role play and storytelling games"}
]
texts = [p["description"] for p in products]
ids = list(range(len(products)))

query= "construction toys"
results= semantic_search(query, texts, ids, model=model, top_k=3, threshold=0.0)
print(f"Query: '{query}'")
for i, score in results:
    print(f"{products[i]['name']} -> {score:.4f}")    