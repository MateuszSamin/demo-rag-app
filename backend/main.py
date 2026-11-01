from fastapi import FastAPI
from api.upload import router as upload_pdf

app = FastAPI()

@app.get("/")
async def root():
    return {
        "message": "Hello World"
    }

app.include_router(upload_pdf)