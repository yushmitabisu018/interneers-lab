import os
from google import genai
from langsmith import traceable
from langsmith.run_helpers import get_current_run_tree
from week8.services.retrieval import retrieve_relevant_chunks

@traceable(name="RAG Pipeline")
def generate_rag_answer(query):
    docs=retrieve_relevant_chunks(query, top_k=3)
    if not docs:
        run_tree= get_current_run_tree()
        trace_url= run_tree.get_url() if run_tree else None
        return "I don't have enough information.", trace_url

    context= "\n\n".join([doc.page_content for doc in docs])

    prompt = f"""
You are an expert assistant.
Answer ONLY using the provided context.
If the answer is not present, say:
"I don't have enough information."

Context:
{context}

Question:
{query}

Answer:
"""
    
    client= genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
    response= client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    run_tree= get_current_run_tree()
    trace_url= run_tree.get_url() if run_tree else None

    return response.text, trace_url
