
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
