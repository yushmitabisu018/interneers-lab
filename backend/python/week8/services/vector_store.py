import os
from langchain_chroma import Chroma
from langchain_core.documents import Document

def create_vector_store(chunks, embedding_model):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    persist_path = os.path.join(base_dir, "chroma_db")

    vectorstore=Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=persist_path
    )
    return vectorstore
