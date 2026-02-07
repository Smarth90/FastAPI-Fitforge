import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from retriever import retrieve


load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
assert GEMINI_API_KEY is not None, "GEMINI_API_KEY not loaded"


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.3,
    api_key=GEMINI_API_KEY
)


PROMPT = ChatPromptTemplate.from_template(
    """
You are FitForge AI, a professional fitness assistant.

Use ONLY the context below to answer the question.
If the answer is not in the context, say:
"I don't have enough information to answer that."

Context:
{context}

Question:
{question}

Answer concisely and clearly.
"""
)


def rag_answer(question: str, k: int = 4) -> str:
    docs = retrieve(question, k=k)
    context = "\n\n".join(doc.page_content for doc in docs)

    messages = PROMPT.format_messages(
        context=context,
        question=question
    )

    response = llm.invoke(messages)
    return response.content


if __name__ == "__main__":
    query = "Give me a beginner workout plan for fat loss"
    print(rag_answer(query))
