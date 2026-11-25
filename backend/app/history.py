from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from .database import (
    get_all_scans,
    get_scan_by_id,
    update_scan,
    delete_scan
)

router = APIRouter()


class ScanUpdate(BaseModel):
    filename: str


# Retrieve all previous scans
@router.get("/scans")
def scan_history():
    return {
        "scans": get_all_scans()
    }


# Retrieve a specific scan
@router.get("/scans/{scan_id}")
def scan_details(scan_id: int):
    scan = get_scan_by_id(scan_id)

    if scan is None:
        raise HTTPException(
            status_code=404,
            detail="Scan not found."
        )

    return scan


# Update a scan record
@router.put("/scans/{scan_id}")
def modify_scan(scan_id: int, data: ScanUpdate):

    filename = data.filename.strip()

    if not filename:
        raise HTTPException(
            status_code=400,
            detail="Filename cannot be empty."
        )

    if not update_scan(scan_id, filename):
        raise HTTPException(
            status_code=404,
            detail="Scan not found."
        )

    return {
        "message": "Scan updated successfully!",
        "scan": get_scan_by_id(scan_id)
    }

# Delete a scan record
@router.delete("/scans/{scan_id}")
def remove_scan(scan_id: int):

    if not delete_scan(scan_id):
        raise HTTPException(
            status_code=404,
            detail="Scan not found."
        )

    return {
        "message": "Scan deleted successfully!",
        "scan_id": scan_id
    }