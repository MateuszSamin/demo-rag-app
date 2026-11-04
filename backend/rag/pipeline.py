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

    sources = [
        {
            "text": chunk["text"],
            "filename": chunk["filename"],
            "document_id": chunk["document_id"],
            "chunk_index": chunk["chunk_index"],
        }
        for chunk in chunks
    ]

    return {
        "answer": answer,
        "sources": sources,
    }