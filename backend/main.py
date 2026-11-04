from fastapi import FastAPI
from api.upload import router as upload_router
from api.chat import router as chat_router

app = FastAPI()

@app.get("/")
async def root():
    return {
        "message": "Hello World"
    }

app.include_router(upload_router)
app.include_router(chat_router)