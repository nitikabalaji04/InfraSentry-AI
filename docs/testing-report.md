# InfraSentry AI – Testing and Debugging Report

## Phase 1 – Day 12

**Intern Name:** Nitika R  
**Program:** UNAI TECH Virtual Internship Program 2026  
**Project:** InfraSentry AI – AI-Powered Infrastructure Security Intelligence Platform  
**Date:** 28 November 2026

## 1. Objective

The objective of Day 12 is to test the implemented functionalities of InfraSentry AI, validate inputs and outputs, identify technical issues and ensure reliable communication between the backend and database.

## 2. Testing Environment

- Operating System: Windows
- Programming Language: Python 3.14.3
- Backend Framework: FastAPI
- Database: SQLite
- Testing Framework: Pytest 9.2.0
- API Testing Tool: FastAPI TestClient
- Development Environment: Visual Studio Code

## 3. Testing Methodology

The following testing approaches were used:

- **Unit Testing:** Testing individual security scanner functions.
- **Functional Testing:** Verifying file uploads, input validation and security detection.
- **Integration Testing:** Verifying communication between backend APIs and the SQLite database.
- **Regression Testing:** Re-executing automated tests after resolving a dependency warning.

Previous frontend integration testing was performed during Day 11. Frontend manual testing was not repeated on Day 12.

## 4. Unit Test Cases

| Test ID | Module | Test Scenario | Input Data | Expected Result | Actual Result | Status |
|---|---|---|---|---|---|---|
| TC01 | Scanner | Root user detection | USER root | High-risk finding | High-risk finding detected | PASS |
| TC02 | Scanner | Latest image detection | python:latest | Medium-risk finding | Medium-risk finding detected | PASS |
| TC03 | Scanner | Hardcoded Docker secret | PASSWORD=demo123 | High-risk finding | Secret detected | PASS |
| TC04 | Scanner | Unrestricted network | 0.0.0.0/0 | High-risk finding | Unrestricted access detected | PASS |
| TC05 | Scanner | Hardcoded Terraform credentials | password="demo123" | High-risk finding | Credentials detected | PASS |
| TC06 | Scanner | Disabled encryption | encrypted=false | High-risk finding | Disabled encryption detected | PASS |
| TC07 | Scanner | Dockerfile without detected issues | Versioned image and non-root user | Zero findings | Zero findings | PASS |
| TC08 | Scanner | Terraform without detected issues | Encryption enabled and restricted network | Zero findings | Zero findings | PASS |

## 5. API and Database Test Cases

| Test ID | Module | Test Scenario | Input Data | Expected Result | Actual Result | Status |
|---|---|---|---|---|---|---|
| TC09 | API | Home endpoint | GET / | HTTP 200 and welcome message | Expected response received | PASS |
| TC10 | API | Health check | GET /health | Healthy status | Healthy status received | PASS |
| TC11 | Upload | Valid Dockerfile | Dockerfile with two detectable issues | Accepted with two findings | Two findings returned | PASS |
| TC12 | Upload | Valid Terraform file | main.tf with encryption disabled | Accepted with high-risk finding | High-risk finding returned | PASS |
| TC13 | Validation | Unsupported file | test.txt | HTTP 400 | HTTP 400 | PASS |
| TC14 | Validation | Empty file | Empty Dockerfile | HTTP 400 | HTTP 400 | PASS |
| TC15 | Validation | Oversized file | File larger than 2 MB | HTTP 400 | HTTP 400 | PASS |
| TC16 | Upload | Duplicate file upload | Same Dockerfile twice | Unique filenames and scan IDs | Unique records and files created | PASS |
| TC17 | Validation | Missing upload file | Request without file | HTTP 422 | HTTP 422 | PASS |
| TC18 | Database | Empty scan history | Empty test database | Empty list | Empty list returned | PASS |
| TC19 | Database | Retrieve scan history | Stored scan record | Record retrieved | Record retrieved | PASS |
| TC20 | Database | Retrieve scan details | Valid scan ID | Scan details and two findings | Expected details returned | PASS |
| TC21 | Database | Update scan | Updated Dockerfile | Filename updated | Filename updated | PASS |
| TC22 | Validation | Invalid filename update | Blank filename | HTTP 400 | HTTP 400 | PASS |
| TC23 | Database | Delete scan | Valid scan ID | Scan and associated findings removed | Scan unavailable and no associated findings returned | PASS |
| TC24 | Analytics | Security summary | One scan with two findings | Correct security statistics | Correct statistics returned | PASS |
| TC25 | Analytics | File type statistics | Dockerfile scan | Correct file type count | Correct count returned | PASS |
| TC26 | Analytics | Severity filtering | HIGH and INVALID | Filtered findings and HTTP 400 for invalid input | Expected responses received | PASS |

## 6. Testing Results

| Testing Category | Executed | Passed | Failed | Execution Time |
|---|---:|---:|---:|---:|
| Scanner Unit Testing | 8 | 8 | 0 | 0.56 seconds |
| API and Database Testing | 18 | 18 | 0 | 3.77 seconds |
| Regression Testing | 26 | 26 | 0 | 2.14 seconds |

**Total Unique Automated Test Cases:** 26

**Final Pass Percentage:** 100%

**Final Warnings:** 0

Regression testing re-executed the same 26 test cases rather than introducing additional unique test cases.

## 7. Issues Identified and Resolved

### Issue 1: Dependency Deprecation Warning

During API testing, a Starlette deprecation warning was displayed regarding the use of HTTPX with TestClient.

**Cause:** The existing HTTPX integration was deprecated by the installed testing framework.

**Solution:** The recommended httpx2 dependency was introduced.

**Retesting:** All 26 automated test cases were executed again.

**Result:** All tests passed without warnings.

**Status:** Resolved.

This was a dependency-related issue rather than an application functionality bug. No application bugs were identified within the executed test cases.

## 8. Test Data Isolation

Automated API tests were configured to use a temporary SQLite database and temporary upload directory.

This ensured that:

- Existing project records were protected.
- Update and delete operations did not affect existing scan history.
- Each API test used an isolated testing environment.
- Test results were independent of existing application data.

## 9. Test Execution Commands

Scanner unit testing:

`python -m pytest tests/test_scanner.py -v`

API and database testing:

`python -m pytest tests/test_api.py -v`

Complete regression testing:

`python -m pytest tests -v`

## 10. Pending Issues and Limitations

- No unresolved failures were observed in the executed automated tests.
- Frontend manual regression testing was not repeated during Day 12.
- Automated browser-based testing can be introduced in future development.
- The current security scanner uses predefined detection rules and may not identify every infrastructure vulnerability.
- Performance, load and comprehensive security testing remain outside the scope of this testing session.

## 11. Conclusion

Day 12 successfully validated the implemented security scanner, backend APIs, database CRUD operations, input validation and security analytics.

All 26 automated test cases passed successfully. A dependency-related warning was identified and addressed, followed by successful regression testing without warnings.

The testing process improved confidence in the implemented functionalities and established a reusable automated testing framework for future development of InfraSentry AI.