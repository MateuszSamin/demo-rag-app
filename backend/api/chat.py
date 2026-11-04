from fastapi import APIRouter
from pydantic import BaseModel

from rag.pipeline import ask

router = APIRouter(prefix="/chat", tags=["chat"])

class ChatRequest(BaseModel):
    question: str

@router.post("/")
def chat(request: ChatRequest):
    answer = ask(request.question)
    return answer