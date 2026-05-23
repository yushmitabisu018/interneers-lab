from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,         
        chunk_overlap=50,       
    )

    chunks = []
    for doc in documents:
        split_texts = splitter.split_text(doc.page_content)
        for chunk in split_texts:
            chunks.append(
                Document(                
                 page_content=chunk,
                 metadata={"source": doc.metadata.get("source", "unknown")}
                ))
    return chunks
