from retrieval.keyword_search import keyword_search
from retrieval.rerank import rerank
from retrieval.vector_search import vector_search

def hybrid_search(question, limit):
    vector_results = vector_search(question, limit * 4)
    keyword_results = keyword_search(question, limit * 4)

    merged = {}

    for chunk in vector_results:
        key = (
            chunk["document_id"],
            chunk["chunk_index"]
        )

        merged[key] = chunk

    for chunk in keyword_results:
        key = (
            chunk["document_id"],
            chunk["chunk_index"]
        )

        if key not in merged:
            merged[key] = chunk

    results = list(merged.values())

    results = rerank(
        question,
        results
    )

    return results[:limit]