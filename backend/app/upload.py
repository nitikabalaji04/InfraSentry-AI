
from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
from uuid import uuid4

router = APIRouter()

MAX_FILE_SIZE = 2 * 1024 * 1024  # 2 MB
CHUNK_SIZE = 64 * 1024  # 64 KB

# Create the uploads directory inside the project root
UPLOAD_DIR = Path(__file__).resolve().parents[2] / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/upload")
async def upload_config(file: UploadFile = File(...)):

    filename = file.filename

    # Check whether filename exists
    if not filename or not filename.strip():
        raise HTTPException(
            status_code=400,
            detail="Filename is required."
        )

    # Extract filename safely
    clean_filename = filename.replace("\\", "/").split("/")[-1]

    # Validate file type
    extension = Path(clean_filename).suffix.lower()

    if clean_filename.lower() != "dockerfile" and extension != ".tf":
        raise HTTPException(
            status_code=400,
            detail="Only Dockerfile and Terraform (.tf) files are supported."
        )

    # Read and validate file size
    total_size = 0
    chunks = []

    while True:
        chunk = await file.read(CHUNK_SIZE)

        if not chunk:
            break

        total_size += len(chunk)

        if total_size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail="File size must not exceed 2 MB."
            )

        chunks.append(chunk)

    # Reject empty files
    if total_size == 0:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty."
        )

    # Generate a unique filename to prevent overwriting
    saved_filename = f"{uuid4().hex}_{clean_filename}"
    file_path = UPLOAD_DIR / saved_filename

    # Save the validated file
    try:
        file_path.write_bytes(b"".join(chunks))
    except OSError:
        raise HTTPException(
            status_code=500,
            detail="Unable to save the uploaded file."
        )

    return {
        "message": "File uploaded, validated, and stored successfully!",
        "original_filename": clean_filename,
        "saved_filename": saved_filename,
        "size_bytes": total_size,
        "file_type": (
            "Dockerfile"
            if clean_filename.lower() == "dockerfile"
            else "Terraform"
        )
    }
