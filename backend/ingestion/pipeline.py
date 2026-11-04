from ingestion.chunker import chunk_pdf
from ingestion.embedder import embed_text
from db.qdrant import store_embeddings, create_collection


def ingest_pdf(pdf_path):
    chunks = chunk_pdf(pdf_path)
    embeddings = embed_text(chunks)

    if embeddings:
        vector_size = len(embeddings[0]["embedding"])
        create_collection(vector_size=vector_size)

    store_embeddings(embeddings)

    return {
        "chunks": len(chunks),
        "vectors": len(embeddings),
    }