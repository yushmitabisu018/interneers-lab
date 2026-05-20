from week8.services.rag import generate_rag_answer
from langsmith import traceable
from langsmith.run_helpers import get_current_run_tree
import re


def _normalize_text(value):
    return " ".join(re.findall(r"[a-z0-9]+", value.lower()))

@traceable(name="Hybrid RAG")
def generate_hybrid_answer(query, products):
    query_lower = query.lower()
    normalized_query = _normalize_text(query)

    #product matching
    product = None
    for p in sorted(products, key=lambda item: len(item.name), reverse=True):
        normalized_name = _normalize_text(p.name)
        if normalized_name and normalized_name in normalized_query:
            product = p
            break

    keywords=["stock", "available", "availability", "inventory"]
    is_stock_query = any(word in query_lower for word in keywords)

    if is_stock_query and product:
        answer= f"Available stock for {product.name} is {product.quantity} units."
        trace_url= None

    elif is_stock_query and not product:
        answer= "I don't have information about that product."
        trace_url= None
    
    else:
        rag_answer,_ = generate_rag_answer(query)
        answer = f"{rag_answer}"
    
    run_tree = get_current_run_tree()
    trace_url = run_tree.get_url() if run_tree else None

    return answer.strip(), trace_url