from langchain_core.documents import Document
import os

def load_documents():
    base_dir =os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path =os.path.join(base_dir, "data")

    documents= []
    for filename in os.listdir(data_path):
        if filename.endswith(".txt"):
            file_path= os.path.join(data_path, filename)

            with open(file_path, "r", encoding="utf-8") as f:
                text =f.read()

                documents.append(
                    Document(
                        page_content=text,
                        metadata={"source": filename}
                    )
                )
    return documents