import os
from langchain_chroma import Chroma
from langsmith import traceable
from langchain_google_genai import ChatGoogleGenerativeAI
from week8.utils.embeddings import get_embedding_model

def load_vector_store():
    base_dir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    persist_path=os.path.join(base_dir, "chroma_db")

    embedding_model= get_embedding_model()
    vectorstore=Chroma(
        persist_directory=persist_path,
        embedding_function=embedding_model
    )
    return vectorstore


@traceable(name="Retrieval Step")
def retrieve_relevant_chunks(query, top_k=3):
    vectorstore = load_vector_store()
    results = vectorstore.similarity_search(query, k=top_k)

    #remove duplicates
    seen =set()
    unique_results=[]

    for doc in results:
        if doc.page_content not in seen:
            seen.add(doc.page_content)
            unique_results.append(doc)

    return unique_results

@traceable(name="LLM Call")
def call_llm(prompt):
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash", 
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0
    )
    response=llm.invoke(prompt)
    return response.content