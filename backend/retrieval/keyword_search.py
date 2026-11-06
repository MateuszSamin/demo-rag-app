from rank_bm25 import BM25Okapi
from db.qdrant import list_chunks

def keyword_search(question, limit=10):
    chunks = list_chunks()

    if not chunks:
        return []

    corpus = [
        chunk["text"].split()
        for chunk in chunks
    ]

    bm25 = BM25Okapi(corpus)

    scores = bm25.get_scores(
        question.split(),
    )

    results = []

    for chunk, score in zip(chunks, scores):
        chunk["score"] = float(score)
        results.append(chunk)

    results.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    return results[:limit]