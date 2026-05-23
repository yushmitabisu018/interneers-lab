import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from week8.utils.document_loader import load_documents
from week8.utils.chunking import split_documents
from week8.utils.embeddings import get_embedding_model
from week8.services.vector_store import create_vector_store
from week8.services.retrieval import retrieve_relevant_chunks

def build_vector_db():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    persist_path = os.path.join(base_dir, "chroma_db")

    if os.path.exists(persist_path):
        print("Vector DB already exists. Skipping rebuild.")
        return

    print("Loading documents...")
    documents = load_documents()

    print("Splitting into chunks...")
    chunks= split_documents(documents)

    print(f"Total chunks created: {len(chunks)}")

    print("Creating embeddings...")
    embedding_model= get_embedding_model()

    print("Storing in vector DB...")
    create_vector_store(chunks, embedding_model)

    print("Vector store created successfully!")

def test_retrieval():
    query = "What's the return policy for damaged items?"
    print("\nQuery:", query)
    results = retrieve_relevant_chunks(query, top_k=3)
    print("\nRetrieved Chunks:\n")

    for i, doc in enumerate(results):
        print(f"--- Chunk {i+1} (Source: {doc.metadata.get('source', 'unknown')}) ---")
        print(doc.page_content)
        print()

def evaluate_retrieval():
    test_cases = [
        {
            "query": "What is the return policy?",
            "expected_source": "return_policy.txt"
        },
        {
            "query": "How to use the toy car?",
            "expected_source": "product_manual.txt"
        },
        {
            "query": "How do vendors get paid?",
            "expected_source": "vendor_faq.txt"
        }
    ]

    print("\nRetrieval Evaluation:\n")

    for test in test_cases:
        results = retrieve_relevant_chunks(test["query"], top_k=1)

        if not results:
            print(f"Query: {test['query']}")
            print("FAIL (No results returned)\n")
            continue

        top_source= results[0].metadata.get("source", "unknown")

        print(f"Query: {test['query']}")
        print(f"Expected: {test['expected_source']}")
        print(f"Got: {top_source}")

        if top_source == test["expected_source"]:
            print("PASS\n")
        else:
            print("FAIL\n")


def main():
    build_vector_db()
    test_retrieval()
    evaluate_retrieval()

if __name__ == "__main__":
    main()    