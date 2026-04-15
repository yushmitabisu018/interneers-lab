from sentence_transformers import SentenceTransformer
import numpy as np

from week7.utils import semantic_search
mini_model= SentenceTransformer('all-MiniLM-L6-v2')
mpnet_model= SentenceTransformer('all-mpnet-base-v2')

products = [
    {"id": "lego_castle_001", "text": "Lego castle building toy for kids"},
    {"id": "lego_city_002", "text": "Lego city construction set"},
    {"id": "wooden_blocks_003", "text": "Wooden blocks for kids learning"},
    {"id": "teddy_bear_010", "text": "Soft teddy bear plush toy"},
    {"id": "action_figure_015", "text": "Superhero action figure"},
    {"id": "soft_blocks_004", "text": "Soft baby blocks for toddlers"},
    {"id": "plush_toy_005", "text": "Soft plush toy gift"},
    {"id": "baby_rattle_006", "text": "Baby rattle toy"},
]
 
texts= [p["text"] for p in products]
ids = [p["id"] for p in products]


query= "toys for 5-year-olds"

print("\nMiniLM Results:")
mini_results= semantic_search(query,texts, ids, mini_model)
for product_id, score in mini_results:
    print(f"{product_id}: {score:.4f}")

print("\nMPNet Results:")
mpnet_results= semantic_search(query,texts, ids, mpnet_model)
for product_id, score in mpnet_results:
    print(f"{product_id}: {score:.4f}")

def manual_rating(results):
    print("\nRate results from 1(bad) to 5(perfect):")
    ratings=[]
    for product_id,_ in results:
        rating= int(input(f"Rating for {product_id}: "))
        ratings.append(rating)

    avg= sum(ratings)/ len(ratings)
    print(f"Average Rating: {avg:.2f}")
    return avg

print("\nRate MiniLM Results:")
mini_avg= manual_rating(mini_results)

print("\nRate MPNet Results:")
mpnet_avg= manual_rating(mpnet_results)
        
