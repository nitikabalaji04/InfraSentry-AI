from fastapi import APIRouter, HTTPException
from .database import get_connection

router = APIRouter()


# Overall security statistics
@router.get("/analytics/summary")
def analytics_summary():
    conn = get_connection()

    try:
        result = conn.execute("""
            SELECT
                COUNT(*) AS total_scans,
                COALESCE(SUM(total_findings), 0) AS total_findings,
                COALESCE(SUM(high_risk), 0) AS high_risk,
                COALESCE(SUM(medium_risk), 0) AS medium_risk
            FROM scans
        """).fetchone()

        return dict(result)

    finally:
        conn.close()


# Scan statistics grouped by file type
@router.get("/analytics/file-types")
def file_type_analytics():
    conn = get_connection()

    try:
        rows = conn.execute("""
            SELECT
                file_type,
                COUNT(*) AS total_scans,
                SUM(total_findings) AS total_findings,
                SUM(high_risk) AS high_risk,
                SUM(medium_risk) AS medium_risk
            FROM scans
            GROUP BY file_type
            ORDER BY file_type
        """).fetchall()

        return {
            "file_types": [dict(row) for row in rows]
        }

    finally:
        conn.close()


# Retrieve and filter security findings
@router.get("/analytics/findings")
def findings_analytics(severity: str | None = None):

    if severity is not None:
        severity = severity.strip().upper()

        if severity not in ("HIGH", "MEDIUM"):
            raise HTTPException(
                status_code=400,
                detail="Severity must be HIGH or MEDIUM."
            )

    conn = get_connection()

    try:
        query = """
            SELECT
                findings.id,
                findings.scan_id,
                scans.filename,
                scans.file_type,
                findings.issue,
                findings.severity,
                findings.recommendation
            FROM findings
            JOIN scans ON findings.scan_id = scans.id
        """

        params = []

        if severity is not None:
            query += " WHERE findings.severity = ?"
            params.append(severity)

        query += " ORDER BY findings.id DESC"

        rows = conn.execute(query, params).fetchall()

        return {
            "total_findings": len(rows),
            "severity_filter": severity,
            "findings": [dict(row) for row in rows]
        }

    finally:
        conn.close()