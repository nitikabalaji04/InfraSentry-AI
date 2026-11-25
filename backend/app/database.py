import sqlite3
from pathlib import Path

# Database file location
DB_PATH = Path(__file__).resolve().parents[2] / "infrasentry.db"


# Establish database connection
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# Initialize database tables
def init_db():
    conn = get_connection()

    try:
        cursor = conn.cursor()

        # Create scans table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS scans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                file_type TEXT NOT NULL,
                total_findings INTEGER NOT NULL,
                high_risk INTEGER NOT NULL,
                medium_risk INTEGER NOT NULL,
                scan_date TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Create findings table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS findings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scan_id INTEGER NOT NULL,
                issue TEXT NOT NULL,
                severity TEXT NOT NULL,
                recommendation TEXT NOT NULL,
                FOREIGN KEY (scan_id) REFERENCES scans(id)
                    ON DELETE CASCADE
            )
        """)

        conn.commit()

    finally:
        conn.close()


# Save security scan results
def save_scan(filename, file_type, findings):
    conn = get_connection()

    try:
        cursor = conn.cursor()

        high_risk = sum(
            f["severity"] == "HIGH" for f in findings
        )

        medium_risk = sum(
            f["severity"] == "MEDIUM" for f in findings
        )

        # Insert scan report
        cursor.execute("""
            INSERT INTO scans (
                filename, file_type, total_findings,
                high_risk, medium_risk
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            filename,
            file_type,
            len(findings),
            high_risk,
            medium_risk
        ))

        scan_id = cursor.lastrowid

        # Insert individual security findings
        for finding in findings:
            cursor.execute("""
                INSERT INTO findings (
                    scan_id, issue, severity, recommendation
                )
                VALUES (?, ?, ?, ?)
            """, (
                scan_id,
                finding["issue"],
                finding["severity"],
                finding["recommendation"]
            ))

        conn.commit()

        return scan_id

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()

# Retrieve all scan reports
def get_all_scans():
    conn = get_connection()

    try:
        rows = conn.execute("""
            SELECT * FROM scans
            ORDER BY id DESC
        """).fetchall()

        return [dict(row) for row in rows]

    finally:
        conn.close()


# Retrieve a specific scan and its findings
def get_scan_by_id(scan_id):
    conn = get_connection()

    try:
        scan = conn.execute(
            "SELECT * FROM scans WHERE id = ?",
            (scan_id,)
        ).fetchone()

        if scan is None:
            return None

        findings = conn.execute(
            "SELECT * FROM findings WHERE scan_id = ?",
            (scan_id,)
        ).fetchall()

        result = dict(scan)
        result["findings"] = [dict(row) for row in findings]

        return result

    finally:
        conn.close()

# Update a scan's filename
def update_scan(scan_id, filename):
    conn = get_connection()

    try:
        cursor = conn.execute("""
            UPDATE scans
            SET filename = ?
            WHERE id = ?
        """, (filename, scan_id))

        conn.commit()

        return cursor.rowcount > 0

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()

# Delete a scan and its associated findings
def delete_scan(scan_id):
    conn = get_connection()

    try:
        cursor = conn.execute(
            "DELETE FROM scans WHERE id = ?",
            (scan_id,)
        )

        conn.commit()

        return cursor.rowcount > 0

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()