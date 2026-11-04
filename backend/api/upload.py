from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, UploadFile, File, HTTPException

from ingestion.pipeline import ingest_pdf

router = APIRouter(prefix="/upload", tags=["upload"])

UPLOAD_DIR = Path("upload")
UPLOAD_DIR.mkdir(exist_ok=True)

@router.post("/")
async def upload_pdf(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="File type is not supported",
        )

    document_id = str(uuid4())

    filename = f"{uuid4()}.pdf"
    file_path = UPLOAD_DIR / filename

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    result = ingest_pdf(pdf_path=file_path, document_id=document_id, filename=file.filename)

    return {
        "message": "File uploaded successfully",
        "filename": file.filename,
        "path": str(file_path),
        **result,
    }