import json
from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"
VECTOR_STORE_DIR = BASE_DIR / "vector_store"

VECTOR_STORE_DIR.mkdir(exist_ok=True)

def load_json_files():
    documents = []

    for file in DATA_DIR.glob("*.json"):
        print(f"Loading {file.name}")
        with open(file , 'r' ,encoding='utf-8') as f:
            data = json.load(f)
            text = (f"Source file: {file.name}\nContent:\n{json.dumps(data, ident = 2)}" )
            documents.append(text)
    return documents

def chunk_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )

    chunks = splitter.create_documents(documents)
    return chunks

def build_vector_store(chunks):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(VECTOR_STORE_DIR)

    print(f"✅ Vector store saved at: {VECTOR_STORE_DIR}")

if __name__ == "__main__":
    print("🚀 Starting RAG ingestion")

    docs = load_json_files()
    print(f"📚 Loaded {len(docs)} documents")

    chunks = chunk_documents(docs)
    print(f"🧩 Created {len(chunks)} chunks")

    build_vector_store(chunks)

    print("🎉 Ingestion complete")