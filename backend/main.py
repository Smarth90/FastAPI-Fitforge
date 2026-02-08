from fastapi import FastAPI
from pydantic import BaseModel
from backend.rag.chain import rag_answer
app = FastAPI(
    title= "FitForge API",
    description= "API for FitForge, your personal fitness assistant.",
    version= "1.0.0"
)

class RAGRequest(BaseModel):
    question: str
    k: int = 4

class RAGResponse(BaseModel):
    answer: str


@app.get("/Active", tags=["Active Check"])
def health_check():
    return {"status": "FitForge API is active and running!"}

@app.post("/rag", response_model=RAGResponse, tags=["RAG"])
def rag_endpoint(request: RAGRequest):
    answer = rag_answer(request.question, k = request.k)
    return {"answer": answer}