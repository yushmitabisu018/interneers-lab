from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

products=[
    "Apple iPhone 17 with advanced camera features",
    "Samsung Galaxy smartphone with AMOLED display",
    "Dell laptop with Intel i7 processor",
    "Nike running shoes for athletes"
]

embeddings = model.encode(products)

for i, emb in enumerate(embeddings):
    print(f"Product: {products[i]}")
    print(f"Vector length: {len(embeddings[i])}")
    print(f"First 5 values: {embeddings[i][:5]}")
    print("-"*50)