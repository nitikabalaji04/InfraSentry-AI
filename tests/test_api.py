import pytest
import sys
from pathlib import Path
from fastapi.testclient import TestClient

# Configure backend import path
sys.path.insert(
    0, str(Path(__file__).resolve().parents[1] / "backend")
)

from app import database, upload


# Create an isolated testing environment
@pytest.fixture
def client(tmp_path, monkeypatch):

    monkeypatch.setattr(
        database, "DB_PATH", tmp_path / "test.db"
    )

    upload_dir = tmp_path / "uploads"
    upload_dir.mkdir()

    monkeypatch.setattr(upload, "UPLOAD_DIR", upload_dir)

    database.init_db()

    from app.main import app

    with TestClient(app) as test_client:
        yield test_client


# Helper function to upload a sample file
def create_scan(client):
    response = client.post(
        "/api/upload",
        files={
            "file": (
                "Dockerfile",
                b"FROM python:latest\nUSER root",
                "text/plain"
            )
        }
    )

    assert response.status_code == 200
    return response.json()


# TC09: Home endpoint
def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Welcome to InfraSentry AI"


# TC10: Backend health
def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


# TC11: Valid Dockerfile upload
def test_dockerfile_upload(client):
    data = create_scan(client)

    assert data["file_type"] == "Dockerfile"
    assert data["security_scan"]["total_findings"] == 2
    assert data["security_scan"]["high_risk"] == 1
    assert data["security_scan"]["medium_risk"] == 1


# TC12: Valid Terraform upload
def test_terraform_upload(client):
    response = client.post(
        "/api/upload",
        files={
            "file": (
                "main.tf",
                b"encrypted = false",
                "text/plain"
            )
        }
    )

    assert response.status_code == 200
    assert response.json()["file_type"] == "Terraform"
    assert response.json()["security_scan"]["high_risk"] == 1


# TC13: Unsupported file type
def test_invalid_file(client):
    response = client.post(
        "/api/upload",
        files={"file": ("test.txt", b"Hello", "text/plain")}
    )

    assert response.status_code == 400


# TC14: Empty file
def test_empty_file(client):
    response = client.post(
        "/api/upload",
        files={"file": ("Dockerfile", b"", "text/plain")}
    )

    assert response.status_code == 400


# TC15: Oversized file
def test_large_file(client):
    response = client.post(
        "/api/upload",
        files={
            "file": (
                "Dockerfile",
                b"A" * (2 * 1024 * 1024 + 1),
                "text/plain"
            )
        }
    )

    assert response.status_code == 400


# TC16: Duplicate upload
def test_duplicate_upload(client):
    first = create_scan(client)
    second = create_scan(client)

    assert first["saved_filename"] != second["saved_filename"]
    assert first["scan_id"] != second["scan_id"]

    assert (upload.UPLOAD_DIR / first["saved_filename"]).exists()
    assert (upload.UPLOAD_DIR / second["saved_filename"]).exists()


# TC17: Missing upload file
def test_missing_file(client):
    response = client.post("/api/upload")
    assert response.status_code == 422


# TC18: Empty scan history
def test_empty_history(client):
    response = client.get("/api/scans")

    assert response.status_code == 200
    assert response.json()["scans"] == []


# TC19: Retrieve stored scan history
def test_scan_history(client):
    data = create_scan(client)
    response = client.get("/api/scans")

    assert response.status_code == 200
    assert any(
        scan["id"] == data["scan_id"]
        for scan in response.json()["scans"]
    )


# TC20: Retrieve individual scan
def test_scan_details(client):
    scan_id = create_scan(client)["scan_id"]
    response = client.get(f"/api/scans/{scan_id}")

    assert response.status_code == 200
    assert response.json()["id"] == scan_id
    assert len(response.json()["findings"]) == 2


# TC21: Update scan record
def test_update_scan(client):
    scan_id = create_scan(client)["scan_id"]

    response = client.put(
        f"/api/scans/{scan_id}",
        json={"filename": "Updated Dockerfile"}
    )

    assert response.status_code == 200

    updated = client.get(f"/api/scans/{scan_id}")
    assert updated.json()["filename"] == "Updated Dockerfile"


# TC22: Reject empty filename update
def test_invalid_update(client):
    scan_id = create_scan(client)["scan_id"]

    response = client.put(
        f"/api/scans/{scan_id}",
        json={"filename": " "}
    )

    assert response.status_code == 400


# TC23: Delete scan and associated findings
def test_delete_scan(client):
    scan_id = create_scan(client)["scan_id"]

    response = client.delete(f"/api/scans/{scan_id}")
    assert response.status_code == 200

    response = client.get(f"/api/scans/{scan_id}")
    assert response.status_code == 404

    findings = client.get("/api/analytics/findings")
    assert findings.json()["total_findings"] == 0


# TC24: Security analytics summary
def test_analytics_summary(client):
    create_scan(client)

    response = client.get("/api/analytics/summary")

    assert response.status_code == 200

    data = response.json()

    assert data["total_scans"] == 1
    assert data["total_findings"] == 2
    assert data["high_risk"] == 1
    assert data["medium_risk"] == 1


# TC25: File type analytics
def test_file_type_analytics(client):
    create_scan(client)

    response = client.get("/api/analytics/file-types")

    assert response.status_code == 200

    data = response.json()["file_types"]

    assert len(data) == 1
    assert data[0]["file_type"] == "Dockerfile"
    assert data[0]["total_scans"] == 1


# TC26: Severity filtering and validation
def test_severity_filter(client):
    create_scan(client)

    response = client.get(
        "/api/analytics/findings?severity=HIGH"
    )

    assert response.status_code == 200
    assert response.json()["total_findings"] == 1

    assert all(
        f["severity"] == "HIGH"
        for f in response.json()["findings"]
    )

    invalid = client.get(
        "/api/analytics/findings?severity=INVALID"
    )

    assert invalid.status_code == 400