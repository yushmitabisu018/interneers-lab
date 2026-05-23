from sentence_transformers import SentenceTransformer
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import numpy as np

from .utils import cosine_similarity

if __name__ == "__main__":
    model = SentenceTransformer('all-MiniLM-L6-v2')
    products=[
        "Lego Castle", 
        "Wooden Blocks", 
        "Action Figure"
    ]

    embeddings = model.encode(products)

    print("Cosine Similarity:")
    for i in range(len(products)):
        for j in range(i+1, len(products)):
            sim= cosine_similarity(embeddings[i], embeddings[j])
            print(f"{products[i]} <-> {products[j]}: {sim:.4f}")

    pca=PCA(n_components=2)
    reduced_embeddings= pca.fit_transform(embeddings)

    plt.figure()

    for i,product in enumerate(products):
        x,y = reduced_embeddings[i]
        plt.scatter(x,y)
        plt.text(x+0.01, y+0.01, product)

    plt.title("2D Visualization of Product Embeddings")
    plt.xlabel("PCA Component 1")
    plt.ylabel("PCA Component 2")
    plt.show()
