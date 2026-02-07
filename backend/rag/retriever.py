from pathlib import Path
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


BASE_DIR = Path(__file__).resolve().parents[2]
VECTOR_STORE_DIR = BASE_DIR / "vector_store"

def load_vector_store():
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    embeddings = HuggingFaceEmbeddings(model_name=model_name)

    vectorstore = FAISS.load_local(VECTOR_STORE_DIR, embeddings, allow_dangerous_deserialization=True)

    return vectorstore

def retrieve(query: str, k: int = 4):
    vectorstore = load_vector_store()
    results = vectorstore.similarity_search(query , k = k)
    return results


if __name__ == "__main__":
    test_query = "Give me a beginner workout plan for weight loss"
    results = retrieve(test_query)
    print(f"Query: {test_query}\n")
    for i, doc in enumerate(results, 1):
        print(f"Result {i}:\n{doc.page_content[:500]}\n{'-'*50}\n")
