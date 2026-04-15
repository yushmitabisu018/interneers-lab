from sentence_transformers import SentenceTransformer
import numpy as np

from week7.utils import semantic_search

model= SentenceTransformer('all-MiniLM-L6-v2')  
products={
   "lego_castle_001": "Lego castle building toy for kids construction play",
    "lego_city_002": "Lego city construction set for building and creativity",
    "wooden_blocks_003": "Wooden blocks building toy for kids construction learning",
    "teddy_bear_010": "Soft teddy bear plush toy for hugging",
    "action_figure_015": "Superhero action figure toy for role play",
    "soft_blocks_004": "Soft baby blocks toy safe for toddlers learning",
    "plush_toy_005": "Soft plush toy gift for toddlers",
    "baby_rattle_006": "Baby rattle toy for infants",
    "puzzle_1000pc_020": "1000 piece puzzle for adults",
    "teen_board_game_025": "Strategy board game for teenagers"
}

product_ids= list(products.keys())
product_description= list(products.values())

search_test_cases=[
   {
        "query": "construction toys",
        "relevant_products": ["lego_castle_001", "lego_city_002", "wooden_blocks_003"],
        "irrelevant_products": ["teddy_bear_010", "action_figure_015"]
    },
    {
        "query": "gifts for toddlers",
        "relevant_products": ["soft_blocks_004", "plush_toy_005", "baby_rattle_006"],
        "irrelevant_products": ["puzzle_1000pc_020", "teen_board_game_025"]
    } 
]

def evaluate_search():
    total_precision=0
    total_recall=0

    for test in search_test_cases:
        query= test["query"]
        relevant= set(test["relevant_products"])

        results= semantic_search(query, product_description, product_ids, model, top_k=5, threshold=0.45, scores=False)
        results_set = set(results)

        tp= len(results_set & relevant)
        precision = tp/len(results)
        recall= tp/len(relevant)

        total_precision+= precision
        total_recall+= recall

        print(f"Query: '{query}'")
        print(f"Results: {results}")
        print(f"Precision: {precision:.2f}")
        print(f"Recall: {recall:.2f}")

    avg_precision= total_precision/ len(search_test_cases)
    avg_recall= total_recall/ len(search_test_cases)
    print(f"\nAverage Precision: {avg_precision:.2f}")
    print(f"Average Recall: {avg_recall:.2f}")

evaluate_search()

