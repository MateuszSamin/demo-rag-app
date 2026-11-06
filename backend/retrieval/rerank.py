from sentence_transformers import CrossEncoder

MODEL = "cross-encoder/ms-marco-MiniLM-L6-v2"

model = CrossEncoder(MODEL)

def rerank(question, chunks):
    if not chunks:
        return []

    pairs = [
        (question, chunk["text"])
        for chunk in chunks
    ]

    scores = model.predict(pairs)

    ranked = []

    for chunk, score in zip(chunks, scores):
        ranked.append({
            **chunk,
            "rerank_score": float(score)
        })

    ranked.sort(
        key=lambda item: item["rerank_score"],
        reverse=True
    )

    return ranked