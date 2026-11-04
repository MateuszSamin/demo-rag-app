from llm.chat import chat
from retrieval.retriever import retrieve

def ask(question: str):
    chunks = retrieve(question)

    context = "\n\n".join(
        chunk["text"]
        for chunk in chunks
    )

    answer = chat(
        question = question,
        context = context,
    )

    return answer