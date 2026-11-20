
from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path

router = APIRouter()

ALLOWED_EXTENSIONS = {".tf", ".dockerfile"}
MAX_FILE_SIZE = 2 * 1024 * 1024  # 2 MB


@router.post("/upload")
async def upload_config(file: UploadFile = File(...)):

    filename = file.filename or ""
    extension = Path(filename).suffix.lower()

    # Validate file type
    if filename.lower() != "dockerfile" and extension != ".tf":
        raise HTTPException(
            status_code=400,
            detail="Only Dockerfile and Terraform (.tf) files are supported."
        )

    # Read uploaded file
    content = await file.read()

    # Validate file size
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="File size must not exceed 2 MB."
        )

    if not content:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty."
        )

    return {
        "message": "File uploaded and validated successfully!",
        "filename": filename,
        "size_bytes": len(content),
        "file_type": "Dockerfile" if filename.lower() == "dockerfile" else "Terraform"
    }
