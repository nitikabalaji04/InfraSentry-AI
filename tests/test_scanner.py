from backend.app.scanner import scan_dockerfile, scan_terraform


# TC01: Detect root user
def test_root_user():
    content = "FROM python:3.11\nUSER root"
    findings = scan_dockerfile(content)

    assert any(
        "root" in f["issue"].lower()
        and f["severity"] == "HIGH"
        for f in findings
    )


# TC02: Detect latest image tag
def test_latest_image():
    content = "FROM python:latest\nUSER appuser"
    findings = scan_dockerfile(content)

    assert any(
        "latest" in f["issue"].lower()
        and f["severity"] == "MEDIUM"
        for f in findings
    )


# TC03: Detect hardcoded Docker secrets
def test_docker_secret():
    content = "FROM python:3.11\nUSER appuser\nENV PASSWORD=demo123"
    findings = scan_dockerfile(content)

    assert any(
        "secret" in f["issue"].lower()
        and f["severity"] == "HIGH"
        for f in findings
    )


# TC04: Detect unrestricted network access
def test_unrestricted_network():
    content = 'cidr_blocks = ["0.0.0.0/0"]'
    findings = scan_terraform(content)

    assert any(
        "unrestricted" in f["issue"].lower()
        and f["severity"] == "HIGH"
        for f in findings
    )


# TC05: Detect hardcoded Terraform credentials
def test_terraform_credentials():
    content = 'password = "demo123"'
    findings = scan_terraform(content)

    assert any(
        "credentials" in f["issue"].lower()
        and f["severity"] == "HIGH"
        for f in findings
    )


# TC06: Detect disabled encryption
def test_disabled_encryption():
    content = "encrypted = false"
    findings = scan_terraform(content)

    assert any(
        "encryption" in f["issue"].lower()
        and f["severity"] == "HIGH"
        for f in findings
    )


# TC07: Dockerfile without detected issues
def test_clean_dockerfile():
    content = "FROM python:3.11\nUSER appuser"
    findings = scan_dockerfile(content)

    assert len(findings) == 0


# TC08: Terraform without detected issues
def test_clean_terraform():
    content = 'encrypted = true\ncidr_blocks = ["10.0.0.0/24"]'
    findings = scan_terraform(content)

    assert len(findings) == 0