import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from backend.rag.retriever import retrieve


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

Use the context below as your ONLY source of truth.
You are allowed to combine and reason across multiple context snippets and use them as well as reason yourself to answer a question.
Do NOT add information that is not supported by the context.
If the context has chunked information, you can combine it to get a more complete picture, but do NOT add any information that is not in the chunks.

If the context is completely irrelevant, say:
"I don't have enough information to answer that."

Context:
{context}

Question:
{question}

Provide a clear, helpful answer.
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
    query = "Give me a workout plan for muscle gain"
    print(rag_answer(query))
