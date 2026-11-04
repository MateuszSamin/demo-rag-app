import ollama

MODEL = "llama3.1:8b"

def chat(question: str, context: str):
    prompt = f"""
        You are only a helpful assistant.
        Answer ONLY using provided context
        
        Context: 
        {context}
        
        Question: 
        {question}
    """

    response = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ]
    )

    return response["message"]["content"]