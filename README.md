
# InfraSentry AI

### AI-Powered Infrastructure Security Intelligence Platform

InfraSentry AI is a project designed to identify security misconfigurations in infrastructure configuration files such as Dockerfiles and Terraform files.

The platform uses security scanning tools to detect potential issues and AI to explain findings, their possible impact, and recommended remediation steps.

## Planned Features

- Infrastructure configuration security scanning
- Security issue detection and severity classification
- AI-powered explanations and recommendations
- Dashboard to display scan results

## Technology Stack

- Python
- FastAPI
- Checkov
- Trivy
- React
- Git and GitHub

## Project Status

Development environment initialized. Implementation is in progress.

## Development Progress

Day 1: Development environment setup completed.
Day 2: Git and GitHub version control setup completed.

## Requirements and Development Plan

The project requirements, features, modules, and development priorities have been documented.

### Main Modules
1. File Upload and Validation
2. Security Scanning Engine
3. Finding Processing and Severity Classification
4. AI Analysis and Recommendation
5. Dashboard and Report Display

### Development Progress
- Day 1: Development environment setup completed.
- Day 2: Git and GitHub version control setup completed.
- Day 4: Requirements analysis and module planning completed.

For detailed requirements, refer to [Requirements Analysis](docs/requirements-analysis.md).

## Phase 1 – Day 5: Initial Implementation

### Module Developed
File Upload and Validation

### Implemented Features
- Upload Dockerfile and Terraform (.tf) configuration files.
- Validate supported file formats.
- Check uploaded file size (maximum 2 MB).
- Reject empty files.
- Display appropriate success and error responses.

### Technology Used
- Python
- FastAPI
- Python Multipart
- Uvicorn

### Testing Results
| Test Case | Result |
|---|---|
| Dockerfile upload | Passed |
| Terraform upload | Passed |
| Unsupported file rejection | Passed |

### Development Progress
- Day 1: Environment setup completed.
- Day 2: Git and GitHub setup completed.
- Day 4: Requirements analysis completed.
- Day 5: File Upload and Validation module implemented and tested.


## Phase 1 – Day 6: Upload Validation and Secure File Storage

### Improvements to File Upload
- Added filename validation to reject missing filenames.
- Improved file type validation to accept only Dockerfile and Terraform (.tf) files.
- Added a 2 MB file size restriction.
- Added empty file validation.
- Used chunk-based reading to check file size.

### New Feature: Secure File Storage
- Added a dedicated `uploads/` directory.
- Validated files are stored locally after successful validation.
- UUID-based filenames prevent existing files from being overwritten.
- Added `uploads/` to `.gitignore` to prevent uploaded files from being pushed to GitHub.

### Testing Performed
| Test | Expected Result | Status |
|---|---|---|
| Dockerfile upload | HTTP 200 | Passed |
| Terraform upload | HTTP 200 | Passed |
| Unsupported .txt file | HTTP 400 | Passed |
| Duplicate filename upload | Unique filename generated | Passed |
| File larger than 2 MB | HTTP 400 | Passed |
| Stored files verification | Files visible in uploads/ | Passed |

### Day 6 Outcome
The file upload module now validates and stores supported infrastructure configuration files. It is ready for integration with the infrastructure security scanning module in the next development phase.

## Day 8 - Infrastructure Security Scanner

### Features Implemented

- Developed a rule-based security scanning module.
- Integrated security scanning with the existing file upload API.
- Added security checks for Dockerfile and Terraform configurations.
- Implemented severity classification and security recommendations.
- Preserved existing file validation and unique file storage.

### Dockerfile Security Checks

- Possible root user execution.
- Usage of the latest image tag.
- Potential hardcoded secrets.

### Terraform Security Checks

- Unrestricted network access.
- Potential hardcoded credentials.
- Disabled encryption.

### Testing Results

| Test Case | Result |
|---|---|
| Existing Dockerfile | 1 high-risk finding |
| Existing Terraform | 0 findings |
| Insecure Dockerfile | 2 high-risk and 1 medium-risk findings |
| Insecure Terraform | 3 high-risk findings |
| Unsupported file | Successfully rejected |

### Challenges Encountered

An indentation error in the upload API initially caused
Dockerfile uploads to return a null response. The issue
was resolved by moving the return statement outside
the conditional block.

### Current Limitations

The scanner uses preliminary rule-based detection.
It is not a comprehensive vulnerability scanner and
may produce false positives or miss security issues.

### Future Improvements

- Expand security detection rules.
- Integrate professional infrastructure scanning tools.
- Implement security risk scoring.
- Develop AI-powered security explanations.
- Build an interactive security dashboard.

## Day 9 - Database Design and Integration

### Database Technology
SQLite was selected because it is lightweight, easy to
integrate with Python, and does not require a separate
database server.

### Implementation Completed

- Designed a relational database schema.
- Established SQLite database connectivity.
- Created scans and findings tables.
- Implemented a one-to-many relationship.
- Integrated database storage with the security scanner.
- Implemented all four CRUD operations.
- Tested CRUD API endpoints using Swagger UI.
- Configured foreign keys and cascade deletion.
- Excluded local database files using .gitignore.

### Database Tables

| Table | Description |
|---|---|
| scans | Stores scan reports and risk summaries |
| findings | Stores individual security findings and recommendations |

### API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | /api/upload | Upload, scan and store results |
| GET | /api/scans | Retrieve all scan reports |
| GET | /api/scans/{scan_id} | Retrieve individual scan details |
| PUT | /api/scans/{scan_id} | Update the displayed filename |
| DELETE | /api/scans/{scan_id} | Delete a scan and its associated findings |

### Database Security

- Parameterized SQL queries
- Foreign key constraints
- Transaction management
- Automatic database connection closure
- Local database files excluded from GitHub

### Challenges Faced

- Encountered a syntax error during database initialization.
- Resolved the issue by correcting the placement of the
  database initialization function in main.py.
- Verified database insertion and retrieval through
  terminal commands and Swagger UI.

### Current Limitations

- Updating a scan modifies only its displayed filename.
- Deleting a scan does not remove the uploaded physical file.
- - Cascade deletion was successfully verified.

### Database Schema

Refer to [Database Schema](docs/database_schema.md)
for the entity relationship diagram and table structure.

## Phase 1 - Day 10: Backend Development and API Integration

### Objective
Develop and integrate backend APIs to retrieve and analyze
security scan data stored in the SQLite database.

### Implemented Features
- Developed a dedicated security analytics module.
- Integrated analytics endpoints with the FastAPI backend.
- Implemented SQL aggregation for overall security statistics.
- Implemented file-type-based analytics.
- Added severity-based filtering of security findings.
- Implemented input validation and error handling.
- Restored the backend health check endpoint.

### New API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /health | Check backend health |
| GET | /api/analytics/summary | Retrieve overall security statistics |
| GET | /api/analytics/file-types | Retrieve file-type-wise statistics |
| GET | /api/analytics/findings | Retrieve and filter security findings |

### Backend and Database Integration
The analytics module uses the existing SQLite database
connection to retrieve scan records and security findings.
SQL aggregation, grouping, joins and parameterized queries
are used to process stored data and return structured
JSON responses.

### API Testing

| Test Case | Expected Status | Result |
|-----------|-----------------|--------|
| Overall security summary | 200 OK | Passed |
| File-type analytics | 200 OK | Passed |
| HIGH severity filtering | 200 OK | Passed |
| Invalid LOW severity | 400 Bad Request | Passed |

All tests were performed using FastAPI Swagger UI.

### Challenges and Solutions
- Avoiding duplication of existing CRUD functionality:
  Created a separate analytics module.
- Handling empty database statistics:
  Used SQL COALESCE to return zero instead of null.
- Handling invalid severity values:
  Implemented input validation with meaningful HTTP
  error responses.
- Maintaining existing functionality:
  Registered the new analytics router without changing
  the database schema.

### Technologies Used
- Python
- FastAPI
- SQLite
- SQL
- Swagger UI
- Git and GitHub

### Outcome
Successfully implemented database-driven security
analytics APIs that provide structured information
for future frontend dashboard integration.

### Future Improvements
- Interactive security analytics dashboard.
- Risk scoring and visualization.
- Scan trends over time.
- AI-generated security recommendations.

## Phase 1 – Day 11: Frontend and Backend Integration

### Objective
Integrate the React frontend with the FastAPI backend and SQLite database to deliver a complete infrastructure security scanning workflow.

### Technologies Used
- React.js – Frontend development
- Vite – Frontend development and build tool
- CSS – Responsive dashboard styling
- FastAPI – Backend API services
- SQLite – Database management
- Fetch API – Frontend and backend communication
- CORS Middleware – Cross-origin communication

### Features Implemented
- Responsive cybersecurity dashboard
- Backend connectivity indicator
- Database-driven security statistics
- Dockerfile and Terraform file uploads
- Frontend file type and size validation
- Security findings with severity levels and recommendations
- Database-driven scan history
- View, rename and delete scan functionality
- Loading states and error messages
- Empty state handling
- Duplicate submission prevention during active requests

### Integrated API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | /health | Backend connectivity |
| POST | /api/upload | Upload and scan configuration files |
| GET | /api/scans | Retrieve scan history |
| GET | /api/scans/{scan_id} | Retrieve individual reports |
| PUT | /api/scans/{scan_id} | Update scan records |
| DELETE | /api/scans/{scan_id} | Delete scan records |
| GET | /api/analytics/summary | Retrieve security statistics |

### Complete Application Workflow

User selects configuration file → Frontend validates input → API receives file → Backend performs security analysis → SQLite stores scan results → Frontend displays security report → Dashboard statistics and scan history are refreshed.

### Testing Results

| Test | Result |
|---|---|
| Backend connectivity | Passed |
| Database statistics retrieval | Passed |
| Dockerfile security scanning | Passed – 3 findings |
| Terraform security scanning | Passed – 3 findings |
| Unsupported file validation | Passed |
| Scan history retrieval | Passed |
| Rename scan record | Passed |
| Delete scan record | Passed |
| Frontend production build | Passed |

### Challenges and Solutions

- Cross-origin communication: Configured CORS middleware to allow communication between the local React frontend and FastAPI backend.
- API integration: Created a centralized API service module to manage requests and responses.
- Invalid file submissions: Implemented frontend validation and meaningful error messages.
- Dashboard synchronization: Implemented automatic data refresh after successful database operations.
- Duplicate submissions: Disabled submission controls while processing requests.

### Running the Application

Start the backend from the project root:

```bash
uvicorn app.main:app --reload --app-dir backend
```

Start the frontend in a separate terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend: http://localhost:5173

Backend: http://127.0.0.1:8000

API Documentation: http://127.0.0.1:8000/docs

### Outcome

Successfully integrated the frontend, backend and database into a functional infrastructure security scanning application. The application supports configuration file analysis, security report visualization and scan record management through a unified dashboard.

The current security scanner uses preliminary rule-based detection and does not guarantee that a configuration is completely secure.