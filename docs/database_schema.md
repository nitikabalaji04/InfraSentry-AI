# InfraSentry AI - Database Schema

## Database Technology
SQLite

## Entity Relationship Diagram

```mermaid
erDiagram
    SCANS ||--o{ FINDINGS : contains

    SCANS {
        INTEGER id PK
        TEXT filename
        TEXT file_type
        INTEGER total_findings
        INTEGER high_risk
        INTEGER medium_risk
        TEXT scan_date
    }

    FINDINGS {
        INTEGER id PK
        INTEGER scan_id FK
        TEXT issue
        TEXT severity
        TEXT recommendation
    }
```

## Database Relationship

The scans and findings tables follow a one-to-many
relationship. Each scan can contain multiple security
findings.

The scan_id foreign key references the id of the
scans table.

ON DELETE CASCADE automatically removes associated
findings when a scan record is deleted.

## Database Operations

- Create: Store security scan results.
- Read: Retrieve scan history and findings.
- Update: Modify the displayed filename.
- Delete: Remove scan records and associated findings.
