from fastapi import FastAPI
from api.upload import router as upload_router
from api.chat import router as chat_router
from api.document import router as document_router

app = FastAPI()

@app.get("/")
async def root():
    return {
        "message": "DEMO RAG APP API"
    }

app.include_router(upload_router)
app.include_router(chat_router)
app.include_router(document_router)